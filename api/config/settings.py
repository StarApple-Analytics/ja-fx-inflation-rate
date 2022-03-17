from os import environ
from dotenv import load_dotenv


# loading env vars from .env file
load_dotenv()



# Redis Config Variables

REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = environ.get("REDIS_PORT")
REDIS_DB = environ.get("REDIS_DB")