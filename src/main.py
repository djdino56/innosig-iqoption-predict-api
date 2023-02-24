import datetime
import logging

from algorithms.neural_prophet import NeuralProphetAlgorithm
from algorithms.prophet import ProphetAlgorithm
from common.enums import KLINE_INTERVAL_1MINUTE, EUR_USD, CAD_JPY, MODEL_REQUEST_CHANNEL
from database.models.base import BaseModel
from database.models.model_result import ModelResult

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
    extractor = IQOptionExtractor()
    dataset = extractor.retrieve(symbol, interval)
    p_algo = ProphetAlgorithm(symbol, interval, dataset)
    p_algo.start()
    n_algo = NeuralProphetAlgorithm(symbol, interval, dataset)
    n_algo.start()


def main():
    # result = ModelResult(**{
    #     "date": datetime.datetime.now(),
    #     "market": "EURUSD",
    #     "interval": "1m",
    #     "algorithm": "prophetalogirthm",
    #     "price": "1.19455546656",
    # })
    # result._id = '63f8cd35abfd85804eb70f69'
    # result.save()
    # found, _result = ModelResult.find("63f8cd35abfd85804eb70f69")
    symbol = EUR_USD
    intervals = [KLINE_INTERVAL_1MINUTE]

    print("== START processing models")
    for interval in intervals:
        print("== Processing model: {} {}".format(symbol, interval))
        execute_single_market(symbol, interval)
        print("== Done processing model: {} {}".format(symbol, interval))
    print("== DONE processing models")


if __name__ == '__main__':
    main()
