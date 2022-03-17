from os import environ
from dotenv import load_dotenv



# loading env vars from .env file
load_dotenv()

class SwaggerConfig(object):
    ''' Base config class. '''
    SWAGGER_URL = '/docs'
    API_URL = "/static/swagger.json"




config = SwaggerConfig