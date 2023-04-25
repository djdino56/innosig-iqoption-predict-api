import logging
from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC

from models.binance.order import Order

BINANCE_SPOT_NAME = 'binance_spot'


class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.logger = logging.getLogger(__name__)
        self._client = Client(api_key=api_key, api_secret=api_secret)
        super().__init__()

    @property
    def exchange_type(self):
        return BINANCE_SPOT_NAME

    def is_active_account(self):
        _response = self._client.get_account_status()
        if 'data' in _response and _response['data'] == 'Normal':
            return True
        else:
            return False

    @property
    def client(self):
        return self._client

    def get_order(self, market: str, order_id: str):
        response = self._client.get_order(symbol=market, orderId=order_id)
        if 'symbol' in response:
            response['market'] = response['symbol']
        return Order(**response)

    def cancel_order(self, market: str, order_id: str):
        response = self._client.cancel_order(symbol=market, orderId=order_id)
        return response

    def place_order(self, market: str, amount: str, price: str, is_buy: bool = True):
        side = 'sell'
        if is_buy:
            side = 'buy'
        if (price is not None) and (amount is not None) and (market is not None) and (side is not None):
            response = self.client.create_order(
                        symbol=market,
                        side=side,
                        type=ORDER_TYPE_LIMIT,
                        timeInForce=TIME_IN_FORCE_GTC,
                        quantity=amount,
                        price=price)
            if 'errorCode' in response:
                return None
            if 'symbol' in response:
                response['market'] = response['symbol']
            _order = Order(**response)
            self.logger.info('++ Created new order ({2}) on market: {0} ({1})'.format(market, side, _order.orderId))
            return _order
