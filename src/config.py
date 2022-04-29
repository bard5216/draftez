import os
from dotenv import load_dotenv

VERSION_NAME = "0.9.0"

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    VERSION = VERSION_NAME

    # Setting the APPLICATION_ROOT config value simply limit Flask's session cookie to that URL prefix.
    # Everything else will be automatically handled for you by Flask and Werkzeug's excellent WSGI handling capabilities.
    # APPLICATION_ROOT = 'draft_sse'

    # Maybe SECRET_KEY should be set in .env
    SECRET_KEY = os.getenv("SECRET_KEY")
    APPLICATION_ROOT = "/draft"
    SCRIPT_NAME = "/draft"

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        # 'pool': QueuePool(creator),
        'pool_size': 4,
        'pool_recycle': 600,
        'pool_pre_ping': True
    }

    # flask-login cookie name
    REMEMBER_COOKIE_NAME = 'draft-sse-login'

    SESSION_COOKIE_NAME = 'draft-sse'
    SESSION_TYPE = "filesystem"

    # Session caching
    # default cache timeout is 28800 seconds = 8 hours if not defined here
    FILESYSTEM_CACHE_DIR = "/var/tmp/python/draft_sse/cache"
    FILESYSTEM_CACHE_TIMEOUT = 28800  # in seconds
    SSE_REDIS_URL = os.getenv('SSE_REDIS_URL')
    # REDIS_URL = "redis:://localhost:6380"


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    ENV = "development"


class DevelopmentConfig(Config):
    ENV = "development"
