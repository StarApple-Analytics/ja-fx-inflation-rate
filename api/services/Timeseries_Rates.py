from api.store.rts import rts


def TimeSeries(key, from_time="-", to_time="+"):
    return {
        "date_ranges": rts.range(key, from_time=from_time, to_time=to_time),
        "metric": "epoch",
    }
