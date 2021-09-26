from dining_hall_api import create_app
from configuration.flask_config import DevelopmentConfig

if __name__ == "__main__":
    app = create_app(config_object=DevelopmentConfig())
    app.run(host='0.0.0.0', port="5001")
