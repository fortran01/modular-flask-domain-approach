# app/__init__.py
from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config
from app.di_container import register_dependencies
from typing import Type
from app.controllers.loyalty_controller import bp as loyalty_bp
from app.controllers.product_controller import bp as product_bp
from app.controllers.customer_controller import bp as customer_bp
from app.utils.error_handlers import (
    handle_validation_error, handle_value_error
)
from pydantic import ValidationError
import logging
from logging.config import dictConfig
from config.logging_config import LOGGING_CONFIG

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()


def create_app(config_class: Type[Config] = Config) -> Flask:
    """
    Create and configure an instance of the Flask application.

    This function initializes a new Flask app, configures it with the provided
    configuration class, sets up the database, marshmallow,
    and migration extensions, registers dependencies, imports and registers
    blueprints, and defines a health check route.

    Args:
        config_class (Type[Config]): The configuration class to use for the
        app. Defaults to the Config class imported from config.config.

    Returns:
        Flask: A configured Flask application instance.
    """
    # Configure logging
    dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)

    app: Flask = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register dependencies
    register_dependencies(app)

    # Register blueprints here
    app.register_blueprint(loyalty_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(customer_bp)

    # Register error handlers
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(ValueError, handle_value_error)

    @app.errorhandler(401)
    def unauthorized(error):
        response = Response(
            jsonify({'error': 'Unauthorized access'}), status=401)
        return response

    @app.route('/health')
    def health_check() -> Response:
        """
        A simple health check endpoint using the Response object.

        Returns:
            Response: A Flask Response object containing the string 'OK'
            and the HTTP status code 200.
        """
        response = Response("OK", status=200)
        return response

    logger.info('Application started')

    return app
