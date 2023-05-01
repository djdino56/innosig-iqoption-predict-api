from datetime import datetime

from database.models.base import BaseModel, Field


class Price(BaseModel):
    _name = "price"
    _name_plural = "prices"
    _collection = "prices"

    _id = Field(name='_id', obj_type=str, is_required=False)
    market = Field(name='market', obj_type=str, is_required=False)
    interval = Field(name='interval', obj_type=str, is_required=False)
    price = Field(name='price', obj_type=float, is_required=False)
    exchange_type = Field(name='exchange_type', obj_type=str, is_required=False)
    is_processed = Field(name='is_processed', obj_type=int, is_required=False)
    _created = Field(name='_created', obj_type=datetime, is_required=False)
    _updated = Field(name='_updated', obj_type=datetime, is_required=False)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._id = args[0]
            self.reload()
        else:
            super().__init__(**kwargs)
