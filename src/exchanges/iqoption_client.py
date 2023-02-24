import logging

from iqoptionapi.stable_api import IQ_Option

from database.models.iqoption.order import Order
from settings import IQ_OPTION_MODE, ALLOWED_INSTRUMENT_TYPES

IQOPTION_NAME = 'iqoption'

logger = logging.getLogger(__name__)


class IQOptionClient:
    def __init__(self, email, password):
        self.logger = logging.getLogger(__name__)
        self._client = IQ_Option(email=email, password=password)
        self.authCheck, self.authData = self._client.connect()
        self._client.change_balance(IQ_OPTION_MODE)
        super().__init__()

    @property
    def exchange_type(self):
        return IQOPTION_NAME

    @property
    def client(self):
        return self._client

    def get_balance(self):
        return self._client.get_balance()

    def get_position_status(self, order_id: str):
        check, data = self._client.get_position(order_id)
        if check:
            return data['position']['status'], data['position']['open_underlying_price']
        else:
            return None

    def get_order(self, market: str, order_id: str):
        check, data = self._client.get_order(order_id)
        if check:
            return Order(**data)
        else:
            return None

    def close_position(self, order_id: str):
        check = self._client.close_position(order_id)
        if check:
            return True
        else:
            return False

    def get_leverage(self, instrument_type, market):
        # "leverage"="Multiplier"
        leverages_valid, leverages = self._client.get_available_leverages(instrument_type, market)
        if leverages_valid:
            return leverages['leverages'][0]['regulated_default']
        else:
            self.logger.error("Wrong leverage")
            return None

    def place_order(self, market: str, amount: str, price: str, profit_value, loss_value, is_buy: bool = True):

        instrument_type = ALLOWED_INSTRUMENT_TYPES[market]

        leverage = self.get_leverage(instrument_type, market)

        if leverage is not None:
            side = 'sell'

            if is_buy:
                side = 'buy'
            if (price is not None) and (amount is not None) and (market is not None) and (side is not None):
                position = {
                    'instrument_id': market,
                    'leverage': leverage,
                    'position_type': side
                }
                _order_id = self.buy_position(self._client, position, instrument_type, amount, loss_value, profit_value)
                if _order_id is None:
                    return None
                # _order = Order(**response)
                self.logger.info('++ Created new order ({2}) on market: {0} ({1})'.format(market, side, _order_id))
                return _order_id
            else:
                return None

    def buy_position(self, client, position, instrument_type, amount, loss_value, profit_value):
        # instrument_type: forex or cfd
        instrument_id = position['instrument_id']  # EUR/USD
        leverage = position['leverage']
        side = position['position_type']  # input:"buy"/"sell"

        ptype = "market"  # input:"market"/"limit"/"stop"

        # for type="limit"/"stop"

        # only working by set type="limit"
        limit_price = None  # input:None/value(float/int)

        # only working by set type="stop"
        stop_price = None  # input:None/value(float/int)

        # "percent"=Profit Percentage
        # "price"=Asset Price
        # "diff"=Profit in Money

        stop_lose_kind = "percent"  # input:None/"price"/"diff"/"percent"
        stop_lose_value = loss_value  # input:None/value(float/int)

        # if instrument_type == InstrumentType.CRYPTO.value:
        #     stop_lose_value = default_loss_value + 20

        take_profit_kind = "percent"  # input:None/"price"/"diff"/"percent"
        take_profit_value = profit_value  # input:None/value(float/int)

        # "use_trail_stop"="Trailing Stop"
        use_trail_stop = False  # True/False

        # "auto_margin_call"="Use Balance to Keep Position Open"
        auto_margin_call = False  # True/False
        # if you want "take_profit_kind"&
        #            "take_profit_value"&
        #            "stop_lose_kind"&
        #            "stop_lose_value" all being "Not Set","auto_margin_call" need to set:True
        use_token_for_commission = False  # True/False
        check, order_id = client.buy_order(instrument_type=instrument_type, instrument_id=instrument_id,
                                           side=side, amount=amount, leverage=leverage,
                                           type=ptype, limit_price=limit_price, stop_price=stop_price,
                                           stop_lose_value=stop_lose_value, stop_lose_kind=stop_lose_kind,
                                           take_profit_value=take_profit_value, take_profit_kind=take_profit_kind,
                                           use_trail_stop=use_trail_stop, auto_margin_call=auto_margin_call,
                                           use_token_for_commission=use_token_for_commission)
        if check:
            logger.debug("Order ID: {}".format(order_id))
            return order_id
        else:
            logger.debug("Something went wrong placing the position")
            return None
