from redistimeseries.client import Client 
from api.config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASS

rts = Client(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS)

