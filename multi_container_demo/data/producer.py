import os
import random
import time

from utils import make_kafka_producer, get_logger

KAFKA_ADDRESS = os.environ["kafka_server"] + ":" + os.environ["kafka_port"]
KAFKA_TOPIC = os.environ["kafka_topic"]

if __name__ == "__main__":
    logger = get_logger()

    # load file of temperatures
    with open("sample_tweets.json", "rb") as f:
        lines = f.readlines()
    f.close()

    # shuffle the order
    random.shuffle(lines)

    # create Kafka producer
    producer = make_kafka_producer(KAFKA_ADDRESS, logger=logger)

    # print a new line every second
    while True:
        for line in lines:
            producer.send(KAFKA_TOPIC,
                          line,
                          timestamp_ms=int(round(time.time() * 1000)))
            logger.info("Sent message to %s", KAFKA_TOPIC)
            seconds_to_wait = random.randint(1, 5)
            time.sleep(seconds_to_wait)
