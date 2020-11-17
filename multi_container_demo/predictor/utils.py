from kafka import KafkaConsumer, KafkaProducer
import logging
import time

def connect_to_kafka(connection_type, address, topic=None, logger=None):
    """
    """
    if logger is None:
        logger = logging.getLogger("default-logger")

    attempted_connections = 0
    connected_to_kafka = False
    connection = None

    logger.info("Creating Kafka connection...")

    while not connected_to_kafka:
        try:
            logger.info("connecting to kafka @ {} attempt #{}".format(address, str(attempted_connections)))

            if connection_type == "consumer":
                connection = KafkaConsumer(topic, bootstrap_servers=[address])
            elif connection_type == "producer":
                connection = KafkaProducer(bootstrap_servers=[address])

            connected_to_kafka = True
            logger.info("Connected to Kafka! Created a producer")
        except Exception as e:
            if attempted_connections < 5:
                attempted_connections += 1
                logger.warning("Failed to connect to kafka at '{}', retrying in 5 seconds (attempt {})".format(address, attempted_connections))
                logger.warning(str(e))
                time.sleep(5)
            else:
                logger.error("Failed to connect to kafka at '{}' after {} retries, exiting".format(address, attempted_connections))
                break

    assert connection, "Couldn't create a kafka producer. Exiting"
    return connection

def make_kafka_consumer(address, topic, logger):
    return connect_to_kafka("consumer", address, topic=topic, logger=logger)

def make_kafka_producer(address, logger):
    return connect_to_kafka("producer", address, topic=None, logger=logger)

def get_kafka_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("kafka-logger")
    return logger