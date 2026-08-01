"""
Test suite for Priority 7: Error Handling, UX Feedback & Observability
"""
import pytest
import json
import os
import tempfile
from flask import g

# Set TESTING before importing app to redirect database
os.environ['TESTING'] = '1'

from utils.errors import error_response, success_response, is_xhr_request
from utils.request_id import generate_request_id


@pytest.fixture(scope='module')
def error_app():
    """Create a fresh test app for error handling tests.
    
    Creates a new Flask app instance to avoid interference with
    the shared app from conftest.py.
    """
    import utils.config
    from flask import Flask, abort
    from routes.workout_plan import workout_plan_bp, initialize_exercise_order
    from routes.workout_log import workout_log_bp
    from routes.main import main_bp
    from routes.filters import filters_bp
    from utils.db_initializer import initialize_database
    from utils.database import add_progression_goals_table, add_volume_tracking_tables
    from utils.errors import register_error_handlers, register_fallback_handlers
    from utils.request_id import add_request_id_middleware
    
    # Use temp test database
    test_db = os.path.join(tempfile.gettempdir(), 'test_error_handling.db')
    original_db = utils.config.DB_FILE
    utils.config.DB_FILE = test_db
    
    # Clean up any existing test database
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create fresh Flask app
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(workout_plan_bp)
    app.register_blueprint(workout_log_bp)
    app.register_blueprint(filters_bp)
    
    # Register middleware and error handlers exactly as app.py does. This fixture
    # used to hand-copy app.py's 404 and catch-all handlers, which could drift
    # from production silently; both now come from the shared registration.
    add_request_id_middleware(app)
    register_error_handlers(app)
    register_fallback_handlers(app)

    # Add error trigger route BEFORE any requests
    @app.route('/__trigger_internal_error')
    def __trigger_internal_error():
        raise RuntimeError('forced test error')

    @app.route('/__trigger_http_error/<int:status_code>')
    def __trigger_http_error(status_code):
        abort(status_code)

    @app.route('/__trigger_api_error')
    def __trigger_api_error():
        from utils.errors import APIError
        raise APIError('TEST_API_ERROR', 'forced API error', 409)

    @app.route('/__post_only', methods=['POST'])
    def __post_only():
        return 'posted'

    @app.route('/__trigger_404_in_message')
    def __trigger_404_in_message():
        # F2: the deleted `"404" in str(e)` branch rendered Not Found for this.
        raise ValueError('bad value 4041')

    # Initialize database within app context
    with app.app_context():
        initialize_database()
        add_progression_goals_table()
        add_volume_tracking_tables()
        initialize_exercise_order()
    
    yield app
    
    # Cleanup
    utils.config.DB_FILE = original_db
    if os.path.exists(test_db):
        os.remove(test_db)


@pytest.fixture
def error_client(error_app):
    """Create a test client for the error test app."""
    with error_app.test_client() as client:
        yield client


class TestRequestIdMiddleware:
    """Test request ID generation and tracking."""
    
    def test_request_id_generated(self, error_client):
        """Test that request ID is automatically generated."""
        response = error_client.get('/')
        assert 'X-Request-ID' in response.headers
        request_id = response.headers.get('X-Request-ID')
        assert request_id.startswith('req_')
    
    def test_request_id_from_header(self, error_client):
        """Test that request ID from header is preserved."""
        custom_id = 'my-custom-request-id'
        response = error_client.get('/', headers={'X-Request-ID': custom_id})
        assert response.headers.get('X-Request-ID') == custom_id
    
    def test_request_id_in_error_response(self, error_client):
        """Test that request ID is included in error responses."""
        response = error_client.get('/nonexistent-route', 
                            headers={'Accept': 'application/json'})
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'requestId' in data.get('error', {})


class TestErrorHandlers:
    """Test error handlers for different HTTP status codes."""
    
    def test_404_json_response(self, error_client):
        """Test 404 handler returns JSON for AJAX requests."""
        response = error_client.get('/nonexistent', 
                            headers={'Accept': 'application/json'})
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['ok'] is False
        assert data['error']['code'] == 'NOT_FOUND'
        assert data['error']['message'] == 'The requested resource was not found'
        assert 'requestId' in data['error']
    
    def test_404_html_response(self, error_client):
        """Test 404 handler returns HTML for browser requests."""
        response = error_client.get('/nonexistent')
        assert response.status_code == 404
        assert response.mimetype == 'text/html'
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data

    def test_500_json_response(self, error_client):
        """Test 500 handler returns JSON for AJAX requests."""
        response = error_client.get('/__trigger_internal_error', headers={'Accept': 'application/json'})
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['ok'] is False
        assert data['error']['code'] == 'INTERNAL_ERROR'
        assert data['error']['message'] == 'An unexpected error occurred'

    def test_500_html_response(self, error_client):
        """Test 500 handler returns HTML for browser requests."""
        response = error_client.get('/__trigger_internal_error', headers={'Accept': 'text/html'})
        assert response.status_code == 500
        assert response.mimetype == 'text/html'
        assert b'Internal Server Error' in response.data

    @pytest.mark.parametrize(('status_code', 'error_code'), [
        (400, 'BAD_REQUEST'),
        (422, 'UNPROCESSABLE_ENTITY'),
        (500, 'INTERNAL_ERROR'),
    ])
    def test_helper_owned_status_handlers_remain_live(
        self, error_client, status_code, error_code
    ):
        response = error_client.get(
            f'/__trigger_http_error/{status_code}',
            headers={'Accept': 'application/json'},
        )
        assert response.status_code == status_code
        assert response.get_json()['error']['code'] == error_code

    def test_api_error_handler_remains_live(self, error_client):
        response = error_client.get(
            '/__trigger_api_error', headers={'Accept': 'application/json'}
        )
        assert response.status_code == 409
        assert response.get_json()['error']['code'] == 'TEST_API_ERROR'

    def test_unrecognized_http_errors_keep_their_own_status(self, error_client):
        """P1/F1. This previously asserted 418 -> 500, characterizing the bug:
        the Exception catch-all owned every HTTPException without a code-keyed
        handler. The generic negotiator now answers with the real status.

        History: added as `test_later_exception_handler_owns_unrecognized_http_errors`
        in 7aee742 (WP0.1, PR #112) to lock a behavior-preserving refactor, not to
        specify a contract. Flipped under APP_PY_REVIEW_PLAN.md decision D3.
        """
        response = error_client.get(
            '/__trigger_http_error/418', headers={'Accept': 'application/json'}
        )
        assert response.status_code == 418
        assert response.get_json()['error']['code'] == 'I_M_A_TEAPOT'

    def test_method_not_allowed_keeps_status_and_allow_header(self, error_client):
        """P1/F1. A GET on a POST-only route is the most reachable case: it used
        to return 500 with a logged stack trace. The `Allow` header is the part a
        bare JSON envelope would silently drop, so assert it on both paths."""
        xhr = error_client.get('/__post_only', headers={'Accept': 'application/json'})
        assert xhr.status_code == 405
        assert xhr.get_json()['error']['code'] == 'METHOD_NOT_ALLOWED'
        assert 'POST' in xhr.headers['Allow']

        browser = error_client.get('/__post_only', headers={'Accept': 'text/html'})
        assert browser.status_code == 405
        assert 'POST' in browser.headers['Allow']

    def test_exception_message_containing_404_still_returns_500(self, error_client):
        """P1/F2. `if "404" in str(e): return handle_404(e)` never fired for a
        genuine NotFound — the code-keyed 404 handler wins first — so it only
        ever misfired, rendering Not Found for unrelated exceptions."""
        response = error_client.get(
            '/__trigger_404_in_message', headers={'Accept': 'application/json'}
        )
        assert response.status_code == 500
        assert response.get_json()['error']['code'] == 'INTERNAL_ERROR'

    def test_negotiator_does_not_steal_code_keyed_statuses(self, error_client):
        """P1 precedence guard. The negotiator and the 400/422/500 handlers
        compete for the same exception class, so status code alone cannot tell
        them apart — a negotiator that stole 500 would still return 500. Assert
        the distinctive message each code-keyed handler produces.
        """
        for status_code, message in (
            (400, 'The request could not be understood or was missing required parameters.'),
            (422, 'The request was well-formed but contained invalid data.'),
            (500, 'An internal server error occurred. Please try again later.'),
        ):
            response = error_client.get(
                f'/__trigger_http_error/{status_code}',
                headers={'Accept': 'application/json'},
            )
            assert response.status_code == status_code
            assert response.get_json()['error']['message'] == message

        not_found = error_client.get('/nonexistent', headers={'Accept': 'application/json'})
        assert not_found.status_code == 404
        assert not_found.get_json()['error']['code'] == 'NOT_FOUND'

    def test_http_error_negotiates_html_for_browser_requests(self, error_client):
        """P1/F1. Browser requests get Werkzeug's own page, not the JSON envelope."""
        response = error_client.get('/__trigger_http_error/403', headers={'Accept': 'text/html'})
        assert response.status_code == 403
        assert response.mimetype == 'text/html'
        assert b'Forbidden' in response.data

    def test_error_response_helper(self, error_app):
        """Test error_response helper function."""
        with error_app.test_request_context():
            # Set request ID
            g.request_id = 'test-request-id'
            
            # Test JSON response (XHR)
            with error_app.test_request_context(headers={'Accept': 'application/json'}):
                g.request_id = 'test-request-id'
                response, status_code = error_response(
                    "TEST_ERROR", 
                    "Test error message", 
                    400
                )
                assert status_code == 400
                data = json.loads(response.data)
                assert data['ok'] is False
                assert data['error']['code'] == 'TEST_ERROR'
                assert data['error']['requestId'] == 'test-request-id'


class TestSuccessResponse:
    """Test success response helper."""
    
    def test_success_response_with_data(self, error_app):
        """Test success response with data."""
        with error_app.test_request_context():
            g.request_id = 'test-request-id'
            response = success_response(data={'key': 'value'}, message='Success')
            
            assert response['ok'] is True
            assert response['data'] == {'key': 'value'}
            assert response['message'] == 'Success'
            assert response['requestId'] == 'test-request-id'
    
    def test_success_response_minimal(self, error_app):
        """Test success response with minimal data."""
        with error_app.test_request_context():
            g.request_id = 'test-request-id'
            response = success_response()
            
            assert response['ok'] is True
            assert response['requestId'] == 'test-request-id'


class TestXHRDetection:
    """Test XHR/AJAX request detection."""
    
    def test_xhr_header_detection(self, error_app):
        """Test detection via X-Requested-With header."""
        with error_app.test_request_context(headers={'X-Requested-With': 'XMLHttpRequest'}):
            assert is_xhr_request() is True
    
    def test_json_accept_detection(self, error_app):
        """Test detection via Accept header."""
        with error_app.test_request_context(headers={'Accept': 'application/json'}):
            assert is_xhr_request() is True
    
    def test_api_path_detection(self, error_app):
        """Test detection via /api/ path."""
        with error_app.test_request_context(path='/api/test'):
            assert is_xhr_request() is True
    
    def test_regular_request(self, error_app):
        """Test regular (non-XHR) request."""
        with error_app.test_request_context():
            assert is_xhr_request() is False


class TestWorkoutLogEndpoints:
    """Test updated workout log endpoints with new error handling."""
    
    def test_update_workout_log_success(self, error_client):
        """Test successful workout log update."""
        # An empty `pass` body counted toward this file's total while asserting
        # nothing. Skipping states the same intent honestly: the happy path needs
        # plan+log fixtures this error-handling app does not build, and it is
        # already covered by tests/test_workout_log_routes.py.
        pytest.skip("happy path covered by test_workout_log_routes.py; this app has no fixtures")
    
    def test_update_workout_log_validation_error(self, error_client):
        """Test workout log update with missing ID."""
        response = error_client.post('/update_workout_log',
                             json={'updates': {'weight': 100}},
                             headers={'Accept': 'application/json'})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['ok'] is False
        assert data['error']['code'] == 'VALIDATION_ERROR'
    
    def test_delete_workout_log_validation_error(self, error_client):
        """Test workout log deletion with missing ID."""
        response = error_client.post('/delete_workout_log',
                             json={},
                             headers={'Accept': 'application/json'})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['ok'] is False
        assert data['error']['code'] == 'VALIDATION_ERROR'


class TestLogging:
    """Test logging with request IDs."""
    
    def test_request_id_in_logs(self, error_client, caplog):
        """Test that request ID appears in log messages."""
        response = error_client.get('/')
        request_id = response.headers.get('X-Request-ID')

        # Previously this computed a `log_contains_request_id` boolean and never
        # asserted it, so the test could not fail. Whether the id reaches caplog
        # depends on handler propagation for the named logger, which this fixture
        # does not control; the contract that is actually this middleware's to
        # keep is that every response carries a well-formed id.
        assert request_id, "no X-Request-ID on the response"
        assert request_id.startswith('req_')


def test_request_id_format():
    """Test request ID format."""
    request_id = generate_request_id()
    assert request_id.startswith('req_')
    assert len(request_id) > 10  # Should have timestamp and random part


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

