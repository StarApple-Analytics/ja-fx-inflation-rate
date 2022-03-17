import os
import logging

from pathlib import Path
from celery.utils.log import get_task_logger
from dotenv import load_dotenv

load_dotenv()

# Loggers
logger = logging.getLogger(__name__)
celeryLogger = get_task_logger(__name__)

# Directory Paths
BASE_DIR = Path.cwd()
RESOURCES_DIR= BASE_DIR /  "api" / "resources"




# Formattings
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DB_RESULT_DATE_TIME_FORMAT = '%Y-%m-%dT%H: %M: %S'



RATES_URL=os.environ.get("RATES_URL", "https://boj.org.jm/statistics/real-sector/inflation/")