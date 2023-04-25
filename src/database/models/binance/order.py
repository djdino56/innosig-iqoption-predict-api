from datetime import datetime
from database.models.base import BaseModel, Field


class Order(BaseModel):
    _name = "order"
    _name_plural = "orders"
    _collection = "orders"

    _id = Field(name='_id', obj_type=str, is_required=False)
    orderId = Field(name='orderId', obj_type=str, is_required=True)
    market = Field(name='market', obj_type=str, is_required=True)
    status = Field(name='status', obj_type=str, is_required=True)
    side = Field(name='side', obj_type=str, is_required=True)
    price = Field(name='price', obj_type=str, is_required=True)
    amount = Field(name='amount', obj_type=str, is_required=False)
    amountRemaining = Field(name='amountRemaining', obj_type=str, is_required=False)
    _created = Field(name='_created', obj_type=datetime, is_required=False)
    _updated = Field(name='_updated', obj_type=datetime, is_required=False)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._id = args[0]
            self.reload()
        else:
            super().__init__(**kwargs)

    def __str__(self):
        return 'Order: {0} | Market: {1} | Status: {2}'.format(
            self.get_field_value('orderId', self._dict),
            self.get_field_value('market', self._dict),
            self.get_field_value('status', self._dict)
        )
