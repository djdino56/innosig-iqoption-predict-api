import logging
from iqoptionapi.stable_api import IQ_Option

from exchanges.singletons.singleton import Singleton
from settings import IQ_OPTION_EMAIL, IQ_OPTION_PASSWORD

IQOPTION_NAME = 'iqoption'


@Singleton
class IQOptionClientSingleton:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._client = IQ_Option(IQ_OPTION_EMAIL, IQ_OPTION_PASSWORD)
        super().__init__()

    @property
    def exchange_type(self):
        return IQOPTION_NAME

    @property
    def client(self):
        return self._client

    # def get_markets(self):
    #     return self._client.markets({})
    #
    # def get_market(self, market: str):
    #     response = self._client.markets({
    #         'market': market
    #     })
    #     return Market(**response)
    #
    # def get_order(self, market: str, order_id: str):
    #     response = self._client.getOrder(market, order_id)
    #     return Order(**response)
    #
    # def cancel_order(self, market: str, order_id: str):
    #     response = self._client.cancelOrder(market, order_id)
    #     return response
    #
    # def get_limit(self):
    #     return self.bitvavo.getRemainingLimit()
    #
    # def get_time(self):
    #     response = self.bitvavo.time()
    #     return ServerTime(**response).__str__()
    #
    # def get_ticker_price_by_market(self, market):
    #     response = self.bitvavo.tickerPrice({'market': market})
    #     return Ticker(**response)

    # def place_order(self, market: str, amount: str, price: str, is_buy: bool = True):
    #     side = 'sell'
    #     if is_buy:
    #         side = 'buy'
    #     if (price is not None) and (amount is not None) and (market is not None) and (side is not None):
    #         # optional parameters: limit:(amount, price, postOnly),
    #         # market:(amount, amountQuote, disableMarketProtection),
    #         # both: timeInForce, selfTradePrevention, responseRequired
    #         response = self.client.placeOrder(market, side, 'limit',
    #                                           {'amount': amount, 'price': price, 'timeInForce': 'GTC'})
    #         if 'errorCode' in response:
    #             return None
    #         _order = Order(**response)
    #         self.logger.info('++ Created new order ({2}) on market: {0} ({1})'.format(market, side, _order.orderId))
    #         return _order
