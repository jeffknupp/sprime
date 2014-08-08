"""This module creates the actual Flask application object."""
from flask import Flask

app = None


def get_app():
    """Return the application instance."""
    global app
    app = Flask(__name__)
    return app
