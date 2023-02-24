from datetime import datetime

from bson import ObjectId

import settings
from database.models.base import BaseModel, Field
from utils.current_date_time import add_timestamps


class ModelResult(BaseModel):
    _name = "model_result"
    _name_plural = "model_results"
    _collection = "model_results"

    _id = Field(name='_id', obj_type=str, is_required=False)
    date = Field(name='date', obj_type=datetime, is_required=True)
    market = Field(name='market', obj_type=str, is_required=True)
    interval = Field(name='interval', obj_type=str, is_required=True)
    algorithm = Field(name='algorithm', obj_type=str, is_required=True)
    price = Field(name='price', obj_type=str, is_required=True)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._id = args[0]
            self.reload()
        else:
            super().__init__(**kwargs)

    def reload(self):
        if self.id:
            if not hasattr(self, '_dict') or self._dict is None:
                self._dict = {}
            self._dict.update(
                self._client[settings.MONGO_DBNAME][self._collection].find_one(
                    {"_id": ObjectId(self.id)}, {"data": {"$slice": -1}}
                )['data'][-1]['content']
            )

    def add_version(self, version: dict):
        result = ModelResult(**version)
        result._id = self.id
        result.save()

    @classmethod
    def find_by_vid(cls, version_id: int):
        _result = cls._client[settings.MONGO_DBNAME][cls._collection].find(
            {"_id": ObjectId(cls.id)},
            {"data": {"$elemMatch": {"vid": version_id}}}
        )
        if _result is not None:
            return True, cls.dict_to_obj(_result['data'][-1]['content'])
        return False, None

    @classmethod
    def find(cls, _id: str):
        _result = cls._client[settings.MONGO_DBNAME][cls._collection].find_one(
            {"_id": ObjectId(_id)},
            {"data": {"$slice": -1}}
        )
        if _result is not None:
            return True, cls.dict_to_obj(_result['data'][-1]['content'])
        return False, None

    def save(self):
        is_update = False
        if self.id is not None:
            is_update = True
        _fields = self.obj_to_dict()
        _fields = add_timestamps(_fields, is_update)
        _fields.pop('_id', None)  # remove _id from the fields

        _current_version = None

        if is_update:
            _current_version = self._client[settings.MONGO_DBNAME][self._collection].find_one(
                {"_id": ObjectId(self.id)},
                {"data": {"$slice": -1}, "data.vid": 1}
            )['data'][-1]

        if not is_update:
            _result = self._client[settings.MONGO_DBNAME][self._collection].insert_one({
                "data": [{
                    "vid": 1,
                    "content": _fields
                }]
            })
            if _result.inserted_id is not None:
                return True, _result.inserted_id
            return False, None
        else:
            _fields = {k: v for k, v in _fields.items() if v is not None}
            _result = self._client[settings.MONGO_DBNAME][self._collection].update(
                {
                    "_id": ObjectId(self.id),
                    "$and": [
                        {"data.vid": {"$not": {"$gt": _current_version["vid"]}}},
                        {"data.vid": _current_version["vid"]}
                    ]
                },
                {"$push": {"data": {"vid": (_current_version["vid"] + 1), "content": _fields}}}
            )
            if _result['updatedExisting'] and _result['nModified'] == 1:
                return True, self.id
            return False, None
