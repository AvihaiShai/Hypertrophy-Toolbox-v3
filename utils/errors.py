"""
Standardized API error responses and helpers.
"""
import re
from typing import Optional, Dict, Any

from flask import jsonify, request, make_response
from werkzeug.exceptions import HTTPException

from utils.request_id import get_request_id


class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def success_response(data: Any = None, message: Optional[str] = None) -> Dict:
    """
    Standard success response format.
    
    Args:
        data: Response data (optional)
        message: Optional success message
    
    Returns:
        Dict with standardized success format
    """
    response = {"ok": True, "status": "success"}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    
    # Add request ID if available
    request_id = get_request_id()
    if request_id:
        response["requestId"] = request_id
    
    return response


def is_xhr_request() -> bool:
    """Determine whether the current request expects a JSON (XHR/API) response."""
    if not request:
        return False

    requested_with = request.headers.get('X-Requested-With', '').lower()
    if requested_with == 'xmlhttprequest':
        return True

    accept_header = request.headers.get('Accept', '')
    if 'application/json' in accept_header.lower():
        return True

    path = getattr(request, 'path', '') or ''
    if path.startswith('/api/'):
        return True

    return False


def error_response(code: str, message: str, status_code: int = 400, **kwargs) -> tuple:
    """
    Standard error response format. Always returns JSON payload expected by API tests.
    
    Args:
        code: Error code (e.g., "VALIDATION_ERROR", "NOT_FOUND")
        message: Error message
        status_code: HTTP status code
        **kwargs: Additional error details
    
    Returns:
        Tuple of (response, status_code)
    """
    from utils.logger import get_logger
    logger = get_logger()
    
    request_id = get_request_id()
    
    # Add request context to error
    endpoint = request.endpoint if request else None
    method = request.method if request else None
    path = request.path if request else None
    user_agent = request.headers.get('User-Agent', '')[:50] if request else None  # Truncate to 50 chars
    
    error_data = {
        "ok": False,
        "status": "error",
        "message": message,
        "error": {
            "code": code,
            "message": message,
            "requestId": request_id,
            **kwargs
        }
    }
    
    # Log error with full context
    logger.error(
        f"API error: {code} - {message}",
        extra={
            'error_code': code,
            'status_code': status_code,
            'endpoint': endpoint,
            'method': method,
            'path': path,
            'user_agent': user_agent,
            'request_id': request_id
        }
    )
    
    return jsonify(error_data), status_code


# Common error codes
ERROR_CODES = {
    "VALIDATION_ERROR": 400,
    "NOT_FOUND": 404,
    "FORBIDDEN": 403,
    "INTERNAL_ERROR": 500,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "UNPROCESSABLE_ENTITY": 422,
}


def _html_error(status_code: int, title: str, message: str):
    """Render the minimal HTML error page used for non-XHR requests."""
    html = (
        "<!DOCTYPE html>"
        "<html lang='en'>"
        f"<head><meta charset='utf-8'><title>{title}</title></head>"
        "<body>"
        f"<h1>{title}</h1>"
        f"<p>{message}</p>"
        "</body></html>"
    )
    response = make_response(html, status_code)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


def register_error_handlers(app):
    """
    Register standardized error handlers for common HTTP errors.

    Args:
        app: Flask application instance
    """
    @app.errorhandler(400)
    def bad_request(e):
        """Handle 400 Bad Request errors."""
        if is_xhr_request():
            return error_response(
                "BAD_REQUEST",
                "The request could not be understood or was missing required parameters.",
                400
            )
        return _html_error(400, "Bad Request", "The request could not be understood or was missing required parameters.")
    
    @app.errorhandler(422)
    def unprocessable_entity(e):
        """Handle 422 Unprocessable Entity errors."""
        if is_xhr_request():
            return error_response(
                "UNPROCESSABLE_ENTITY",
                "The request was well-formed but contained invalid data.",
                422
            )
        return _html_error(422, "Unprocessable Entity", "The request was well-formed but contained invalid data.")
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 Internal Server errors."""
        # Get request context for logging
        request_id = get_request_id()
        endpoint = request.endpoint if request else None
        method = request.method if request else None
        path = request.path if request else None
        user_agent = request.headers.get('User-Agent', '')[:50] if request else None
        
        # Log the error with full context
        app.logger.exception(
            f"Internal server error",
            extra={
                'status_code': 500,
                'endpoint': endpoint,
                'method': method,
                'path': path,
                'user_agent': user_agent,
                'request_id': request_id
            }
        )
        
        if is_xhr_request():
            return error_response(
                "INTERNAL_ERROR",
                "An internal server error occurred. Please try again later.",
                500
            )
        return _html_error(500, "Internal Server Error", "An internal server error occurred. Please try again later.")
    
    @app.errorhandler(APIError)
    def handle_api_error(e):
        """Handle custom APIError exceptions."""
        return error_response(e.code, e.message, e.status_code)


def _http_error_code(e: HTTPException) -> str:
    """Derive an envelope error code from a Werkzeug exception name.

    ``MethodNotAllowed`` -> ``METHOD_NOT_ALLOWED``. Non-alphanumerics collapse to
    underscores so names like "I'm a Teapot" still yield a usable code.
    """
    return re.sub(r'[^A-Z0-9]+', '_', (e.name or '').upper()).strip('_') or 'HTTP_ERROR'


def register_fallback_handlers(app):
    """Register the fallback layer: 404, the generic HTTP negotiator, and the
    unhandled-exception catch-all.

    These own whatever the code-keyed handlers in ``register_error_handlers``
    do not. Kept separate from that function so its 400/422/500/APIError
    contract is unchanged, and shared so ``app.py`` and the priority-7 test
    fixture register identical layering instead of hand-copying it.

    Register this *after* ``register_error_handlers(app)``. Flask resolves a
    handler by trying the code-keyed map first and then walking the exception's
    MRO against the class-keyed map, so the 400/422/500/APIError handlers still
    win for their own statuses; only unclaimed HTTP errors reach the negotiator.
    """
    from utils.logger import get_logger
    logger = get_logger()

    @app.errorhandler(404)
    def handle_404(error):
        """Handle 404s without logging a stack trace for common missing files."""
        del error  # Flask supplies the exception, but this handler needs only the request.
        if request.path == '/favicon.ico':
            return make_response('', 204)

        logger.warning(f"404 Not Found: {request.path}")
        if is_xhr_request():
            return error_response("NOT_FOUND", "The requested resource was not found", 404)
        return _html_error(404, "Not Found", "The requested resource was not found.")

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Answer HTTP errors that have no dedicated handler with their own status.

        Without this, 405/413/403 and friends fall through to the ``Exception``
        catch-all below and are reported as 500. Browser requests get Werkzeug's
        own response untouched; XHR requests get the standard JSON envelope plus
        the exception's headers, which is how ``Allow`` survives on a 405.
        """
        if not is_xhr_request():
            return e

        status_code = e.code or 500
        payload, _ = error_response(_http_error_code(e), e.description or e.name, status_code)
        response = make_response(payload, status_code)
        for key, value in e.get_response().headers:
            if key.lower() not in ('content-type', 'content-length'):
                response.headers.add(key, value)
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Global handler for genuinely unhandled exceptions; always a 500."""
        import sys
        import traceback

        # Log to both logger and stderr for export routes
        if hasattr(e, '__class__'):
            print(f"=== EXCEPTION: {e.__class__.__name__}: {e} ===", file=sys.stderr, flush=True)
            traceback.print_exc(file=sys.stderr)

        logger.exception(f"Unhandled exception: {e}")

        if is_xhr_request():
            return error_response("INTERNAL_ERROR", "An unexpected error occurred", 500)
        return _html_error(500, "Internal Server Error", "An unexpected error occurred.")
