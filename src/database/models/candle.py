import settings
from database.models.base import BaseModel, Field


class Candle(BaseModel):
    _name = "candle"
    _name_plural = "candles"
    _collection = "candles"

    _id = Field(name='_id', obj_type=str, is_required=False)
    date = Field(name='date', obj_type=str, is_required=True)
    market = Field(name='market', obj_type=str, is_required=True)
    interval = Field(name='interval', obj_type=str, is_required=True)
    trend = Field(name='trend', obj_type=float, is_required=True)
    yhat_lower = Field(name='yhat_lower', obj_type=float, is_required=True)
    yhat_upper = Field(name='yhat_upper', obj_type=float, is_required=True)
    trend_lower = Field(name='trend_lower', obj_type=float, is_required=True)
    trend_upper = Field(name='trend_upper', obj_type=float, is_required=True)
    multiplicative_terms = Field(name='multiplicative_terms', obj_type=float, is_required=True)
    multiplicative_terms_lower = Field(name='multiplicative_terms_lower', obj_type=float, is_required=True)
    multiplicative_terms_upper = Field(name='multiplicative_terms_upper', obj_type=float, is_required=True)
    additive_terms = Field(name='additive_terms', obj_type=float, is_required=True)
    additive_terms_lower = Field(name='additive_terms_lower', obj_type=float, is_required=True)
    additive_terms_upper = Field(name='additive_terms_upper', obj_type=float, is_required=True)
    yhat = Field(name='yhat', obj_type=float, is_required=True)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._id = args[0]
            self.reload()
        else:
            super().__init__(**kwargs)

    @classmethod
    def find_by_date(cls, date: str, market: str, interval: str):
        _result = cls._client[settings.MONGO_DBNAME][cls._collection].find_one({"date": date,
                                                                                "market": market,
                                                                                "interval": interval})
        if _result is not None:
            return True, cls.dict_to_obj(_result)
        return False, _result
