from celery import Celery
from celery.schedules import crontab

from dotenv import load_dotenv


from api import create_worker_app
from api.config.celeryConfig import config 
from api.tasks import scrape_inflation

load_dotenv()



def create_celery(app):
    celery = Celery(
        app.import_name,
    )


    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_worker_app()
celery = create_celery(flask_app)
celery.config_from_object(config)



