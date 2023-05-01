import time

import socketio
import logging

from settings import REDIS_HOST, REDIS_PORT
from algorithms.neural_prophet import NeuralProphetAlgorithm
from algorithms.prophet import ProphetAlgorithm
from common.enums import KLINE_INTERVAL_1MINUTE, BTC_USDT, MODEL_REQUEST_CHANNEL
from database.models.base import BaseModel
from database.models.price import Price
from exchanges.singletons.binance_client_singleton import BINANCE_SPOT_NAME
from extractor.binance import BinanceExtractor

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)-8s  %(message)s',
                    datefmt='(%H:%M:%S)')
logger = logging.getLogger(__name__)


def set_model_request_in_queue(symbol, interval):
    return BaseModel.set_in_queue({
        "symbol": symbol,
        "interval": interval,
    }, channel=MODEL_REQUEST_CHANNEL)


def execute_single_market(symbol, interval, mgr=None):
    logger.debug("== Scheduling model: {} {}".format(symbol, interval))
    # extractor = IQOptionExtractor()
    extractor = BinanceExtractor()
    dataset = extractor.retrieve(symbol, interval)
    p_algo = ProphetAlgorithm(symbol, interval, dataset)
    p_algo.start(mgr)
    n_algo = NeuralProphetAlgorithm(symbol, interval, dataset)
    n_algo.start(mgr)


def main():
    market = BTC_USDT
    intervals = [KLINE_INTERVAL_1MINUTE]

    while True:
        for interval in intervals:
            _price = Price.find_one({
                "exchange_type": BINANCE_SPOT_NAME,
                "interval": interval,
                "market": market,
                "is_processed": 0
            })

            if _price:
                print("== Processing model: {} {}".format(market, interval))
                mgr = socketio.RedisManager('redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT))
                execute_single_market(market, interval, mgr)
                print("== Done processing model: {} {}".format(market, interval))
                _price.is_processed = 1  # signal processed!
                _price.save()
        time.sleep(5)


if __name__ == '__main__':
    main()
