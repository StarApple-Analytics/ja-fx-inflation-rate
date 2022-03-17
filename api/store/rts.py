from redistimeseries.client import Client 
from api.config.settings import REDIS_HOST, REDIS_PORT

rts = Client(host=REDIS_HOST, port=REDIS_PORT)

