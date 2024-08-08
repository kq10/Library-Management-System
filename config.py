class Config(object):
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    CACHE_TYPE = 'SimpleCache'  # Use SimpleCache as a fallback if Redis is not configured
    CACHE_DEFAULT_TIMEOUT = 300  # Default cache timeout (in seconds)

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SECRET_KEY = 'thisissecret'
    SECURITY_PASSWORD_SALT = 'thisissalt'
    CACHE_TYPE = 'RedisCache'  # Uncomment if you want to use Redis for caching
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0  # Use default Redis database

def get_config(env):
    """Utility function to get the appropriate config class based on environment."""
    config_classes = {
        'development': DevelopmentConfig,
    }
    return config_classes.get(env, DevelopmentConfig)  # Default to DevelopmentConfig
