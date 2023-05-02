import time
import logging

from binance import ThreadedWebsocketManager
from binance.enums import KLINE_INTERVAL_1MINUTE

from settings import BINANCE_API_KEY, BINANCE_SECRET_KEY
# from sockets.process import send_message_all

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)-8s  %(message)s',
                    datefmt='(%H:%M:%S)')
logger = logging.getLogger(__name__)


def handle(response):
    print("PRICE_UPDATE", response)


if __name__ == '__main__':
    # send_message(sid, 'data', {'data': 'foobar'})
    logger.debug("=======================")
    logger.debug("Starting socket servers...")
    logger.debug("=======================")
    logger.debug("Subscribing markets..")
    _markets = [
        {'base': 'BTCUSDT',
         'interval': KLINE_INTERVAL_1MINUTE}
    ]
    logger.debug("Starting threadedWebsocketManager..")
    # Starting the WebSocket, is required to initialise its internal loop
    threadedWebsocketManager = ThreadedWebsocketManager(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
    threadedWebsocketManager.start()
    logger.debug("Started threadedWebsocketManager..")
    # Define the streams!
    streams = []
    for _market in _markets:
        socket_name = '{}@kline_{}'.format(_market['base'].lower(), _market['interval'])
        logger.debug(".. socket subscribing: {} ..".format(socket_name))
        streams.append(socket_name)
    threadedWebsocketManager.start_multiplex_socket(callback=handle, streams=streams)
    timeout = 5  # seconds
    time.sleep(timeout)
    # send_message_all("RUN_UPDATE", "starting")
    threadedWebsocketManager.join(timeout=timeout)
    time.sleep(timeout)
