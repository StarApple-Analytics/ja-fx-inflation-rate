import logging.config
from os import environ
from celery import Celery
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from .store.rts import rts
from .config.appConfig import config as app_config
from .config.celeryConfig import config as celery_config
from .config.swaggerConfig import SwaggerConfig as swaggerConfig
from .constant import logger


def create_app():

    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])

    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        swaggerConfig.SWAGGER_URL,
        swaggerConfig.API_URL,
        config={"app_name": "JA FX API"},
    )

    # Plugins initialization goes here
    CORS(app, resources={r"/*": {"origins": "*"}})

    # --------------------------------
    # Module Imports
    # --------------------------------

    # Import the module / component using their blueprints
    from api.routes import API_ROUTES

    # Register Blueprints

    for api_blueprint in API_ROUTES:
        app.register_blueprint(api_blueprint, url_prefix="/api/")

    # Register Swagger Blueprint
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix="/docs/")

    @app.before_request
    def before_request():

        try:
            rts.create(
                "MONTHLYINFLATION:JA",
                labels={
                    "SYMBOL": "JA_MONTHLY_INFLATION",
                    "DESC": "MONTHLY_FX_INFLATION_JA",
                    "TIMEFRAME": "1_MONTH",
                    "COUNTRYNAME": "JAMAICA",
                },
            )
        except Exception as e:
            logger.error(e)

    @app.route("/")
    def toDocs():
        return redirect("/docs/")

    return app


def create_worker_app():
    """Minimal App without routes for celery worker."""
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])
    app.config.from_object(celery_config)

    return app


def get_environment():
    return environ.get("APPLICATION_ENV") or "development"
