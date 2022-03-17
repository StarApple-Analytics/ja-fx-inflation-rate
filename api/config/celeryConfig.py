from kombu import Queue, Exchange
from celery.schedules import crontab
from dotenv import load_dotenv
from datetime import timedelta
from os import environ
from api.constant import BASE_DIR
from celery.schedules import crontab

load_dotenv()


class CeleryConfig(object):

    """Celery Config Class"""

    APP_NAME = environ.get("CELERY_APP_NAME", "API Celery Worker")
    REDIS_HOST = environ.get("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = environ.get("REDIS_CONTAINER_PORT", 6379)
    result_expires = 30
    timezone = "UTC"
    broker_url = environ.get("broker_url")
    result_backend = environ.get(
        "BROKER_URL",
        "redis://{host}:{port}/0".format(host=REDIS_HOST, port=str(REDIS_PORT)),
    )
    accept_content = ["json", "msgpack", "yaml"]
    task_serializer = "json"
    result_serializer = "json"
    CELERY_LOG_FILE = (BASE_DIR / "log" / "celery.log").absolute().as_posix()
    imports = "api.tasks"
    task_queues = (Queue("default", Exchange("default"), routing_key="default"),)

    CELERY_LOGGING = {
        "format": "[%(asctime)s] - %(name)s - %(levelname)s - " "%(message)s",
        "datefmt": "%b %d %Y %H:%M:%S",
        "filename": CELERY_LOG_FILE,
        "maxBytes": 10000000,  # 10megabytes
        "backupCount": 5,
    }

    task_routes = {
        "api.tasks.scrape_inflation.scrape": {
            "queue": "default",
            "routing_key": "default",
        },
    }

    beat_schedule = {
        "monthly-scraping": {
            "task": "api.tasks.scrape_inflation.scrape",
            "schedule":600,
        }
    }


config = CeleryConfig
