import datetime as dt
import logging
import numpy as np
import os
import random

logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel("INFO")

STDEV_THRESHOLD = os.environ.get("stdev_threshold", 1)

def get_data_from_last_n_hours(num_hours):
    run_timestamp = dt.datetime.now().replace(minute=0, second=0, microsecond=0)
    values = []
    for minute in range(0, 60*num_hours):
        ts = run_timestamp - dt.timedelta(minutes=minute)
        values.append((ts, random.random()))
    return values[::-1]

def detect_anomalies(value_data):
    values = [value for (minute, value) in value_data]
    avg_val = np.mean(values)
    stdev = np.std(values)

    labelled_values = [(minute, value, abs(value - avg_val) > stdev*STDEV_THRESHOLD) for (minute, value) in value_data]
    return labelled_values

def write_out_predictions(labelled_data):
    only_anom = [(ts, val) for (ts, val, anom) in labelled_data if anom]
    for (timestamp, value) in only_anom:
        logger.info("ANOMALY: {} - {}".format(timestamp, value))
    logger.info("Wrote {} anomalous points to file".format(len(only_anom)))


if __name__ == "__main__":
    data = get_data_from_last_n_hours(3)
    anom_data = detect_anomalies(data)
    write_out_predictions(anom_data)
