from database.models.base import BaseModel, Field


class Market(BaseModel):
    _name = "market"
    _name_plural = "markets"
    _collection = "markets"

    market = Field(name='market', obj_type=str, is_required=True)
    status = Field(name='status', obj_type=str, is_required=True)
    base = Field(name='base', obj_type=str, is_required=True)
    quote = Field(name='quote', obj_type=str, is_required=True)
    exchange = Field(name='exchange', obj_type=str, is_required=True)
    pricePrecision = Field(name='pricePrecision', obj_type=int, is_required=True)
    minOrderInQuoteAsset = Field(name='minOrderInQuoteAsset', obj_type=str, is_required=True)
    minOrderInBaseAsset = Field(name='minOrderInBaseAsset', obj_type=str, is_required=False)
    stepSize = Field(name='stepSize', obj_type=str, is_required=False)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._id = args[0]
            self.reload()
        else:
            super().__init__(**kwargs)

    @staticmethod
    def binance_market(response: dict):
        _price_filter = next((item for item in response['filters'] if item["filterType"] == "PRICE_FILTER"), None)
        _qt_filter = next((item for item in response['filters'] if item["filterType"] == "LOT_SIZE"), None)
        if _price_filter:
            _market = Market(**{
                'exchange': response['exchange'],
                'market': response['symbol'],
                'status': response['status'],
                'base': response['baseAsset'],
                'quote': response['quoteAsset'],
                'pricePrecision': response['baseAssetPrecision'],
                'minOrderInQuoteAsset': _price_filter['minPrice'],
                'minOrderInBaseAsset': _qt_filter['minQty'],
                'stepSize': _qt_filter['stepSize']
            })
            return _market
        return None

    def __str__(self):
        return 'Market: {} | Base: {} | Quote: {} | Status: {}'.format(
            self.get_field_value('market', self._dict),
            self.get_field_value('base', self._dict),
            self.get_field_value('quote', self._dict),
            self.get_field_value('status', self._dict)
        )
