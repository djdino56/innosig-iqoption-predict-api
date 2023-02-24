from datetime import datetime
from models.base import BaseModel, Field


class Order(BaseModel):
    _name = "order"
    _name_plural = "orders"
    _collection = "orders"

    _id = Field(name='_id', obj_type=str, is_required=False)
    orderId = Field(name='orderId', obj_type=str, is_required=True)
    status = Field(name='status', obj_type=str, is_required=True)
    market = Field(name='market', obj_type=str, is_required=True)
    _created = Field(name='_created', obj_type=datetime, is_required=False)
    _updated = Field(name='_updated', obj_type=datetime, is_required=False)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._id = args[0]
            self.reload()
        elif 'id' in kwargs and 'instrument_id' in kwargs:
            kwargs['orderId'] = kwargs['id']
            kwargs['market'] = kwargs['instrument_id']
            super().__init__(**kwargs)
        else:
            super().__init__(**kwargs)

    def __str__(self):
        return 'Order: {0} | Market: {1} | Status: {2}'.format(
            self.get_field_value('orderId', self._dict),
            self.get_field_value('market', self._dict),
            self.get_field_value('status', self._dict)
        )
