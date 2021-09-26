class FlaskConfig(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(FlaskConfig):
    DEBUG = False
    SECRET_KEY = "9asdf8980as8df9809sf6a6ds4f3435fa64ˆGggd76HSD57hsˆSDnb"


class DevelopmentConfig(FlaskConfig):
    ENV = "development"
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = "secret_for_test_environment"
