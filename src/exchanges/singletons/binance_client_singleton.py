import logging
from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC

from database.models.binance.order import Order

from exchanges.singletons.singleton import Singleton
from settings import BINANCE_SECRET_KEY, BINANCE_API_KEY

BINANCE_SPOT_NAME = 'binance_spot'


@Singleton
class BinanceClientSingleton:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
        super().__init__()

    @property
    def exchange_type(self):
        return BINANCE_SPOT_NAME

    @property
    def client(self):
        return self._client

    def get_order(self, market: str, order_id: str):
        response = self._client.get_order(symbol=market, orderId=order_id)
        return response

    def cancel_order(self, market: str, order_id: str):
        response = self._client.cancel_order(symbol=market, orderId=order_id)
        return response

    def get_markets(self):
        res = self._client.get_exchange_info()
        return res['symbols']

    def place_test_order(self, market: str, amount: str, is_buy: bool = True):
        side = 'sell'
        if is_buy:
            side = 'buy'
        if (amount is not None) and (market is not None) and (side is not None):
            response = self.client.create_test_order(
                symbol=market,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=amount)
            if 'errorCode' in response:
                return None
            if 'symbol' in response:
                response['market'] = response['symbol']
            _order = Order(**response)
            self.logger.info('++ Created new order ({2}) on market: {0} ({1})'.format(market, side, _order.orderId))
            return _order
