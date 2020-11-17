from utils import make_kafka_consumer, get_kafka_logger
import logging
import os
import time

KAFKA_ADDRESS = os.environ["kafka_server"] + ":" + os.environ["kafka_port"]
KAFKA_TOPIC = os.environ["kafka_topic"]

if __name__ == "__main__":
    logger = get_kafka_logger()

    consumer = make_kafka_consumer(KAFKA_ADDRESS, KAFKA_TOPIC, logger)

    for message in consumer:
        logger.info(message)