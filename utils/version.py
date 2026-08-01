"""Single source of the application version.

Kept in Python rather than read from ``package.json`` so a frozen build and a
source checkout report the same value with no build step and no Node dependency
at runtime. ``app.py`` exposes it to templates as ``app_version``, which every
first-party CSS/JS link uses as its ``?v=`` cache buster.

Keep in step with ``package.json``'s ``"version"``; ``tests/test_version.py``
fails if the two drift apart.
"""

APP_VERSION = "3.0.1"
