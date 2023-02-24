from pymongo import MongoClient

import settings
import logging

logger = logging.getLogger(__name__)


class HubbleMongoClient:
    _name = ""
    _name_plural = ""
    _collection = ""
    _mongo_uri = settings.MONGO_URI
    _client = MongoClient(_mongo_uri)
