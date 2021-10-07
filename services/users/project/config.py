import os


class BaseConfig:
    """
        Base Configuration
    """
    TESTING = False 
    JSONIFY_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'birth_is_death'
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevelopmentConfig(BaseConfig):
    """
        Development Configuration   
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """
        Testing Configuration
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    DEBUG_TB_ENABLED = True


class ProductionConfig(BaseConfig):
    """
        Production Configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
