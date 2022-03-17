from os import environ
from api.constant import BASE_DIR
from dotenv import load_dotenv



# loading env vars from .env file
load_dotenv()

class BaseConfig(object):
    ''' Base config class. '''

    APP_NAME = environ.get('APP_NAME', 'JA FX INFLATIION RATE API')
    ORIGINS = ['*']
    EMAIL_CHARSET = 'UTF-8'
    
    SECRET_KEY = environ.get("SECRET_KEY", None)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    RESULTS_PER_API_CALL = 25

    LOG_INFO_FILE = (BASE_DIR / "log" / "info.log").absolute().as_posix()

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] - %(name)s - %(levelname)s - '
                '%(message)s',
                'datefmt': '%b %d %Y %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'log_info_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_INFO_FILE,
                'maxBytes': 16777216,  # 16megabytes
                'formatter': 'standard',
                'backupCount': 5
            },
        },
        'loggers': {
            APP_NAME: {
                'level': 'DEBUG',
                'handlers': ['log_info_file'],
            },
        },
    }



class Development(BaseConfig):
    ''' Development config. '''

    DEBUG = True
    ENV = 'dev'
    SECRET_KEY = environ.get('SECRET_KEY') or "$UPER$ECRET_KEY"
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URL')


class Staging(BaseConfig):
    ''' Staging config. '''

    DEBUG = True
    ENV = 'staging'


class Production(BaseConfig):
    ''' Production config '''

    DEBUG = False
    ENV = 'production'


config = {
    'development': Development,
    'staging': Staging,
    'production': Production,
}