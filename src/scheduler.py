#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import functools
import threading

from main import set_model_request_in_queue
from services import scheduler
from common.enums import KLINE_INTERVAL_1MINUTE, EUR_USD

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)-8s  %(message)s',
                    datefmt='(%H:%M:%S)')
logger = logging.getLogger(__name__)


def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        logger.info('LOG: Job "%s" completed' % func.__name__)
        return result

    return wrapper


@with_logging
def execute_markets(symbol, interval):
    job_thread_comparer = threading.Thread(target=set_model_request_in_queue, args=[symbol, interval])
    job_thread_comparer.start()


def main():
    symbol = EUR_USD
    interval = KLINE_INTERVAL_1MINUTE

    logger.debug('Pre-scheduling tasks...')

    logger.debug("== START scheduling")
    scheduler.every().minute.at(":59").do(execute_markets, symbol=symbol, interval=interval)
    logger.debug("== DONE scheduling")

    logger.debug('Running scheduler now...')
    scheduler.run_continuously()


if __name__ == "__main__":
    main()
