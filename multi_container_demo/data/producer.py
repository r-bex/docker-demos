import datetime as dt
from utils import make_kafka_producer, get_kafka_logger
import json
import logging
import os
import time

KAFKA_ADDRESS = os.environ["kafka_server"] + ":" + os.environ["kafka_port"]
KAFKA_TOPIC = os.environ["kafka_topic"]

def parse_line(lb):
    # decode bytes to string, chop of \r\n at back and split by tab delimiter
    line_parts = lb.decode("utf-8")[:-2].split("\t")
    timestamp_str = " ".join(line_parts[0:2])
    return str.encode(json.dumps({
        "timestamp": timestamp_str,
        "temperature": float(line_parts[2])
    }))

if __name__ == "__main__":
    logger = get_kafka_logger()
    
    # load file of temperatures
    with open("temp_data.txt", "rb") as f:
        lines = f.readlines()
    f.close()

    # create Kafka producer
    producer = make_kafka_producer(KAFKA_ADDRESS, logger=logger)
    
    # print a new line every second
    for line in lines:
        producer.send(
            KAFKA_TOPIC,
            parse_line(line), 
            timestamp_ms=int(round(time.time() * 1000))
        )
        logger.info(f"Sent message to {KAFKA_TOPIC}")
        time.sleep(1)
    