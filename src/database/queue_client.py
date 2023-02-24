import random
import string
from pymongo import MongoClient
from mongo_queue.queue import Queue

import settings
import logging

logger = logging.getLogger(__name__)


def get_random_string(length=8):
    # With combination of lower and upper case
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


class HubbleQueueClient:
    _name = ""
    _name_plural = ""
    _collection = ""
    _mongo_uri = settings.MONGO_URI
    _consumer_id = "consumer-{}".format(get_random_string())
    logger.debug("Consumer name generated: {}".format(_consumer_id))
    _queue_client = Queue(MongoClient(_mongo_uri)[settings.MONGO_DBNAME].tasks_queue,
                          consumer_id=_consumer_id,
                          timeout=300,
                          max_attempts=3)
