"""This module creates the actual Flask application object."""

# Third-party imports
from flask import Flask

app = None


def get_app():
    """Return the application instance."""
    global app  # pylint: disable=global-statement
    app = Flask(__name__)
    return app
