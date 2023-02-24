#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
from bson import json_util

from common.enums import MODEL_REQUEST_CHANNEL
from database.models.base import BaseModel
from database.models.objects.model_request import ModelRequest
from main import execute_single_market


def start_logging():
    consumer_id = BaseModel.get_consumer_id()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)-8s  %(message)s',
                        datefmt='(%H:%M:%S)')
    logger = logging.getLogger(__name__)
    logger.info("=======================")
    logger.info("Running consumer '%s'" % consumer_id)
    logger.info("=======================")
    return logger


def main():
    logger = start_logging()
    while True:
        job = BaseModel.next_from_queue(channel=MODEL_REQUEST_CHANNEL)
        if job is not None:
            request = ModelRequest(**json_util.loads(job.payload))
            execute_single_market(request.symbol, request.interval)
            # Job is complete!
            job.complete()
        else:
            logger.info("============= Sleeping for %d seconds" % 5)
            time.sleep(5)


if __name__ == '__main__':
    main()
