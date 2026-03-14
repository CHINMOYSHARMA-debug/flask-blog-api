from flasgger import Swagger
from app import app

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint" : 'apispec',
            "route" : '/apispec.json',
            "rule_filter" : lambda rule: True,
            "model_filter" : lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Blog API",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <your_token>"
        }
    },
    "security": [
        {
            "Bearer": []
        } 
    ]
}

Swagger(app, config=swagger_config, template=swagger_template)

