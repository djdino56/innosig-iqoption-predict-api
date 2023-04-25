import datetime
import logging

from algorithms.neural_prophet import NeuralProphetAlgorithm
from algorithms.prophet import ProphetAlgorithm
from common.enums import KLINE_INTERVAL_1MINUTE, BTC_USDT, MODEL_REQUEST_CHANNEL
from database.models.base import BaseModel
from extractor.binance import BinanceExtractor

from extractor.iqoption import IQOptionExtractor

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


def execute_single_market(symbol, interval):
    logger.debug("== Scheduling model: {} {}".format(symbol, interval))
    # extractor = IQOptionExtractor()
    extractor = BinanceExtractor()
    dataset = extractor.retrieve(symbol, interval)
    p_algo = ProphetAlgorithm(symbol, interval, dataset)
    p_algo.start()
    n_algo = NeuralProphetAlgorithm(symbol, interval, dataset)
    n_algo.start()


def main():
    symbol = BTC_USDT
    intervals = [KLINE_INTERVAL_1MINUTE]

    print("== START processing models")
    for interval in intervals:
        print("== Processing model: {} {}".format(symbol, interval))
        execute_single_market(symbol, interval)
        print("== Done processing model: {} {}".format(symbol, interval))
    print("== DONE processing models")


if __name__ == '__main__':
    main()
