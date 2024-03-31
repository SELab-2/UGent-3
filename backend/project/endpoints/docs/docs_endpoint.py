"""
Module for defining the swagger docs
"""

from os import getenv
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = getenv("DOCS_URL")
API_URL = getenv("DOCS_JSON_PATH")

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    f"/{API_URL}",
    config={
        'app_name': 'Pigeonhole API'
    }
)
