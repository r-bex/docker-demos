import json
import os
import random
import preprocessor as p

from utils import make_kafka_consumer, get_logger

KAFKA_ADDRESS = os.environ["kafka_server"] + ":" + os.environ["kafka_port"]
KAFKA_TOPIC = os.environ["kafka_topic"]


def preprocess_tweet(tweet_string):
    # apply preprocessor library to remove tags, urls etc
    cleaned_string = p.clean(tweet_string)
    # remove punctuation
    for punc_to_remove in [".",",","!","?"]:
        cleaned_string = cleaned_string.replace(punc_to_remove, "")
    # additionally, everything lowercase and  remove any words that aren't entirely alphanumeric
    words = [w.lower() for w in cleaned_string.split(" ") if w.isalpha()]
    return " ".join(words)


class TweetLanguageClassifier():
    def __init__(self, language_words):
        self.corpus = self._load_corpus(language_words)

    def _load_corpus(self, raw_words):
        # bytes to string and strip newlines
        return [w.decode("utf-8").replace("\n", "") for w in raw_words]

    def predict(self, tweet_text, prob_threshold=0.5):
        if len(tweet_text) == 0:
            return -1

        tweet_words = tweet_text.split(" ")
        language_counts = [int(tw in self.corpus) for tw in tweet_words]
        language_probability = sum(language_counts) / len(tweet_words)

        if language_probability >= prob_threshold:
            return 1
        else:
            return 0


if __name__ == "__main__":
    logger = get_logger()

    # read in list of common words and use to init Classifier
    with open("corpus.txt", "rb") as f:
        common_words = f.readlines()
    f.close()
    classifier = TweetLanguageClassifier(common_words)

    # set up a Kafka consumer
    consumer = make_kafka_consumer(KAFKA_ADDRESS, KAFKA_TOPIC, logger)

    for message in consumer:
        message_data = json.loads(message.value.decode("utf-8"))
        logger.info("Raw text: {}".format(message_data["data"]["text"]))

        cleaned_text = preprocess_tweet(message_data["data"]["text"])
        logger.info("Cleaned text: {}".format(cleaned_text))

        prediction = classifier.predict(cleaned_text)
        prediction_text_map = {
            1: "English",
            0: "not English",
            -1: "n/a"
        }
        logger.info("Prediction: {} ({})".format(prediction, prediction_text_map[prediction]))