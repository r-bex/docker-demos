import datetime as dt
import logging
import numpy as np
import random

from utils import make_hour_data, condense_anomalous_periods

logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel("INFO")

def get_data_from_last_n_hours(num_hours):
    start_of_current_hour = dt.datetime.now().replace(minute=0, second=0)
    hour_starts = [start_of_current_hour - dt.timedelta(hours=h) for h in range(num_hours, 0, -1)]
    logger.info("Loading data for {} hours: {}".format(num_hours, str(hour_starts)))
    
    total_values = []
    for hour_start in hour_starts:
        hour_values = make_hour_data(hour_start)
        total_values += hour_values
    return total_values

def detect_anomalies(value_data):
    values = [value for (minute, value) in value_data]
    avg_val = np.mean(values)
    stdev = np.std(values)

    labelled_values = [(minute, value, abs(value - avg_val) > stdev*1) for (minute, value) in value_data]
    return labelled_values

def write_out_predictions(labelled_data):
    condensed_periods = condense_anomalous_periods(labelled_data)
    for (start, end) in condensed_periods:
        logger.info("{} - {}".format(start, end))
    logger.info("Wrote {} anomalous periods to file".format(len(condensed_periods)))


if __name__ == "__main__":
    data = get_data_from_last_n_hours(3)
    anom_data = detect_anomalies(data)
    write_out_predictions(anom_data)
