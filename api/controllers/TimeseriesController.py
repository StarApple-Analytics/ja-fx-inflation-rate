from flask import request
from api.services import Timeseries_Rates
from operator import itemgetter


def index():

    from_time, to_time = itemgetter("from_time", "to_time")(request.args)

    if int(from_time) == 0:
        from_time = "-"

    if int(to_time) == 0:
        to_time = "+"
        
    return Timeseries_Rates.TimeSeries(
        "MONTHLYINFLATION:JA", from_time=from_time, to_time=to_time
    )
