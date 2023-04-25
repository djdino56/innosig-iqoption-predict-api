from exchanges.binance_client import BinanceClient
from database.models.base import BaseModel, Field


class Balance(BaseModel):
    asset = Field(name='asset', obj_type=str, is_required=True)
    free = Field(name='free', obj_type=float, is_required=True)
    locked = Field(name='locked', obj_type=float, is_required=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_balance(exchange: BinanceClient, symbol):
        response = exchange.client.get_asset_balance(asset=symbol)
        return Balance(**response)

    def enough_current_balance(self, compared_balance=10):
        if self.get_current() > compared_balance:
            return True
        else:
            return False

    def get_current(self):
        return self.get_field_value('free', self._dict)

    def get_total(self):
        return self.get_field_value('free', self._dict) + self.get_field_value('locked', self._dict)

    def __str__(self):
        return 'Symbol: {0} | Current balance: €{1} | In order: €{2}'.format(
            self.get_field_value('asset', self._dict),
            self.get_field_value('free', self._dict),
            self.get_field_value('locked', self._dict)
        )
