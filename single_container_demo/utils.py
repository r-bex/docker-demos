import random

direction_transition_probs = {
    1: [0.6, 0.7],
    0: [0.4, 0.6],
    -1: [0.4, 0.5]
}

def _get_new_direction(current_direction):
    (threshold1, threshold2) = direction_transition_probs[current_direction]
    rand = random.random()
    if rand < threshold1:
        return 1
    elif rand >= threshold1 and rand < threshold2:
        return 0
    else:
        return -1

def make_hour_data(hour_start):
    current_number = random.randint(1,100)
    current_direction = 0

    values = []
    for minute in range(0,60):
        new_direction = _get_new_direction(current_direction)
        interval = random.randint(1,5)
        new_number = current_number + new_direction*interval
        ts = hour_start.replace(minute=minute)
        values.append((ts, new_number))

    assert len(values) == 60
    return values

def condense_anomalous_periods(labelled_values):
    anomalous_periods = []
    currently_anom = False
    anom_start = None

    for (minute, value, anomalous) in labelled_values:
        if not currently_anom and anomalous:
            # start tracking a new anomalous zone
            anom_start = minute
            currently_anom = True
        elif currently_anom and not anomalous:
            # anomalous zone has ended
            anomalous_periods.append((anom_start, minute))
            currently_anom = False
            
    return anomalous_periods

