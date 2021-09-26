from flask import Flask
from .views import dining_hall


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.register_blueprint(dining_hall)
    return app
