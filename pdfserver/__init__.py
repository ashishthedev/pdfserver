import logging
from logging.handlers import RotatingFileHandler

from flask import Flask


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    handler = RotatingFileHandler('logs.log', maxBytes=100*1000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # Register the api blueprint.
    from .webapp import webapp
    app.register_blueprint(webapp, url_prefix='')

    from .api import api
    app.register_blueprint(api, url_prefix='/api')

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
