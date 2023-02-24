import settings
from database.models.base import BaseModel, Field


class Market(BaseModel):
    _name = "market"
    _name_plural = "markets"
    _collection = "markets"

    _id = Field(name='_id', obj_type=str, is_required=False)
    market = Field(name='market', obj_type=str, is_required=True)
    interval = Field(name='interval', obj_type=str, is_required=True)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._id = args[0]
            self.reload()
        else:
            super().__init__(**kwargs)

    @classmethod
    def find_by_market_interval(cls, symbol: str, interval: str):
        _result = cls._client[settings.MONGO_DBNAME][cls._collection].find_one({"symbol": symbol,
                                                                                "interval": interval})
        if _result is not None:
            return True, cls.dict_to_obj(_result)
        return False, _result
