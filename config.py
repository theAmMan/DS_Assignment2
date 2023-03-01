class configuration:
    """base virual class"""

class production_config(configuration):
    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost:5432/broker_manager"
    )
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = "development"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost:5432/broker_manager"
    )
    DEBUG = True
    TESTING = True