import logging
import socketio
import requests

from database.models.price import Price
from exchanges.singletons.binance_client_singleton import BINANCE_SPOT_NAME
from settings import REDIS_HOST, REDIS_PORT

from binance.exceptions import BinanceAPIException
from requests import ReadTimeout
from binance import ThreadedWebsocketManager
from binance.enums import KLINE_INTERVAL_1MINUTE

from settings import BINANCE_API_KEY, BINANCE_SECRET_KEY


def price_update(response):
    market = response['data']["s"]
    interval = response['data']["k"]["i"]
    close = response['data']["k"]["c"]
    _price = Price(**{
        'market': market,
        'interval': interval,
        'is_processed': 0,
        'exchange_type': BINANCE_SPOT_NAME,
        'price': close
    })
    # Delete all previous signals
    _old_price = Price.find_one({
        'market': market,
        'exchange_type': BINANCE_SPOT_NAME,
        'interval': interval
    })
    if _old_price is None:
        _id = _price.save()
    else:
        _old_price.price = close
        _old_price.is_processed = 0
        _old_price.save()
        _id = _old_price.id
    return Price.find_one({
        '_id': _id
    })


def handle(response):
    if "e" in response and response['e'] == 'error':
        if "m" in response:
            logging.getLogger(__name__).error(
                'error: {}'.format(response['m']))
        logging.getLogger(__name__).error(
            'error: close and restart the socket')
    else:
        try:
            if "data" in response and "s" in response["data"]:
                pair = response['data']["s"]
                interval = response['data']["k"]["i"]
                close = response['data']["k"]["c"]
                logging.getLogger(__name__).info(
                    'new socket message received - {} - {} - {} - {}'.format(response['data']["e"],
                                                                             pair,
                                                                             interval,
                                                                             close))
                mgr = socketio.RedisManager('redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT))
                mgr.emit('PRICE_UPDATE', data=response)
                price_update(response)
                # results = execute_single_market(pair, interval, mgr)
        except KeyError as e:
            logging.getLogger(__name__).error(
                'error: keyerror occurred, restarting websocket')
        except (ValueError, ReadTimeout, BinanceAPIException, requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError) as err:
            logging.getLogger(__name__).error(err)
            logging.getLogger(__name__).error(
                'error: something went wrong, skipping error')


if __name__ == '__main__':
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)-8s  %(message)s',
                        datefmt='(%H:%M:%S)')
    logger = logging.getLogger(__name__)
    logger.debug("=======================")
    logger.debug("Starting socket servers...")
    logger.debug("=======================")
    logger.debug("Subscribing markets..")
    _markets = [
        {'base': 'BTCUSDT',
         'interval': KLINE_INTERVAL_1MINUTE}
    ]
    # Starting the WebSocket, is required to initialise its internal loop
    threadedWebsocketManager = ThreadedWebsocketManager(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
    threadedWebsocketManager.start()
    # Define the streams!
    streams = []
    for _market in _markets:
        socket_name = '{}@kline_{}'.format(_market['base'].lower(), _market['interval'])
        logger.debug(".. socket subscribing: {} ..".format(socket_name))
        streams.append(socket_name)
    threadedWebsocketManager.start_multiplex_socket(callback=handle, streams=streams)
    timeout = 5  # seconds
    threadedWebsocketManager.join(timeout=timeout)
