from database.models.base import BaseModel, Field


class Account(BaseModel):
    _name = "account"
    _name_plural = "accounts"
    _collection = "accounts"

    _id = Field(name='_id', obj_type=str, is_required=False)
    name = Field(name='name', obj_type=str, is_required=True)
    token = Field(name='token', obj_type=str, is_required=True)
    roles = Field(name='roles', obj_type=dict, is_required=False, is_list=True)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._id = args[0]
            self.reload()
        else:
            super().__init__(**kwargs)
