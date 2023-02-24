from bson import json_util

import settings
import pymongo
from bson.objectid import ObjectId

from datetime import datetime

from database.mongo_client import HubbleMongoClient
from database.queue_client import HubbleQueueClient
from utils.current_date_time import add_timestamps


class BaseModel(HubbleMongoClient, HubbleQueueClient):

    def __init__(self, *args, _dict=None, **kwargs):
        super().__init__()
        if _dict is None:
            _dict = {}
        self._dict = _dict
        self.set_fields(**kwargs)

    @classmethod
    def get_consumer_id(cls):
        return cls._consumer_id

    @classmethod
    def set_in_queue(cls, json, priority=1, channel=None, depends_on=[]):
        if channel is None:
            channel = cls.__name__
        return cls._queue_client.put(json_util.dumps(json, sort_keys=True, indent=None),
                                     priority=priority,
                                     channel=channel,
                                     depends_on=depends_on)

    @classmethod
    def next_from_queue(cls, channel=None):
        if channel is None:
            channel = cls.__name__
        return cls._queue_client.next(channel=channel)

    def set_model_in_queue(self, priority=1):
        self._queue_client.put(self.to_json(indent=None), priority=priority, channel=self.__class__.__name__)

    def to_json(self, indent=4):
        return json_util.dumps(self.obj_to_dict(), sort_keys=True, indent=indent)

    @classmethod
    def get_collection(cls):
        return cls._client[settings.MONGO_DBNAME][cls._collection]

    def get_last_from_db(self):
        _doc = self._client[settings.MONGO_DBNAME][self._collection].find_one(
            sort=[("id", pymongo.DESCENDING)]
        )
        if _doc is not None:
            return self.dict_to_obj(_doc)
        return None

    def save(self):
        is_update = False
        _fields = self.obj_to_dict()
        if self.id is not None:
            is_update = True
        _fields = add_timestamps(_fields, is_update)
        _fields.pop('_id', None)  # remove _id from the fields
        if not is_update:
            _result = self._client[settings.MONGO_DBNAME][self._collection].insert_one(_fields)
            if _result.inserted_id is not None:
                return _result.inserted_id
        else:
            _fields = {k: v for k, v in _fields.items() if v is not None}
            _result = self._client[settings.MONGO_DBNAME][self._collection].update_one({"_id": ObjectId(self.id)},
                                                                                       {'$set': _fields}, upsert=True)
            if _result.acknowledged is True and _result.matched_count == 1:
                return _result.acknowledged
        return None

    def reload(self):
        if self.id:
            self._dict.update(
                self._client[settings.MONGO_DBNAME][self._collection].find_one({"_id": ObjectId(self.id)}))

    def remove(self):
        if self.id:
            self._client[settings.MONGO_DBNAME][self._collection].remove({"_id": ObjectId(self.id)})
            self._dict.clear()

    @classmethod
    def find_by_id(cls, _id: str):
        _result = cls._client[settings.MONGO_DBNAME][cls._collection].find_one({"_id": ObjectId(_id)})
        if _result is not None:
            return True, cls.dict_to_obj(_result)
        return False, _result

    def set_fields(self, **kwargs):
        for field in dir(self):
            field_type = self.__getattribute__(field)
            if type(field_type) == Field:
                self.__setattr__(self._field_type_name(field), field_type)
                value = self.get_field_value(field, kwargs)
                self.__setattr__(field, value)
                self._dict[field] = value
                field_type.validate(value)

    @staticmethod
    def _field_type_name(name):
        return "__type_{}".format(name)

    def get_field_type(self, name):
        return self.__getattribute__(self._field_type_name(name))

    def set_field_type(self, name, value):
        self.set_fields(**{
            name: value
        })

    # ToDO cast str to int and vice versa
    def get_field_value(self, field_name, values):
        value = values.get(field_name, None)
        if value:
            field_type = self.get_field_type(field_name)
            if type(value) == dict:
                if issubclass(field_type.obj_type, BaseModel):
                    value = field_type.obj_type.dict_to_obj(value)
            elif field_type.is_list:
                new_value = []
                for sub_val in value:
                    if type(sub_val) == dict and issubclass(field_type.obj_type, BaseModel):
                        new_value.append(field_type.obj_type.dict_to_obj(sub_val))
                    else:
                        new_value.append(sub_val)
                value = new_value
            elif type(value) != field_type.obj_type and value is not None:
                value = field_type.try_cast(value)
        return value

    @classmethod
    def dict_to_obj(cls, value):
        return cls(**value)

    def obj_to_dict(self):
        new_dict = {}
        for field in self._dict.keys():
            value = self.__getattribute__(field)
            if isinstance(value, BaseModel):
                new_dict[field] = value.obj_to_dict()
            elif isinstance(value, list):
                new_dict[field] = []
                for list_obj in value:
                    if isinstance(list_obj, BaseModel):
                        new_dict[field].append(list_obj.obj_to_dict())
                    else:
                        new_dict[field].append(list_obj)
            else:
                new_dict[field] = value
        return new_dict

    @property
    def id(self):
        if hasattr(self, "_id"):
            return self._id
        return None

    @property
    def updated_at(self):
        if hasattr(self, "_id") and hasattr(self, "_updated"):
            if self._dict['_updated'] is not None:
                return self._dict['_updated'].astimezone().isoformat()
        return None

    @classmethod
    def find_one(cls, _filter: dict):
        if '_id' in _filter:
            _filter['_id'] = ObjectId(_filter['_id'])
        _result = cls._client[settings.MONGO_DBNAME][cls._collection].find_one(
            _filter, sort=[("timestamp", pymongo.DESCENDING)])
        if _result is not None:
            return cls.dict_to_obj(_result)
        else:
            return None

    @classmethod
    def find_all_unlimited(cls, _filter: dict = {}):
        for _key in _filter:
            if '_id' in _key:
                if isinstance(_filter[_key], str) or isinstance(_filter[_key], bytes) or isinstance(_filter[_key],
                                                                                                    ObjectId):
                    _filter[_key] = ObjectId(_filter[_key])
        _results = list(cls._client[settings.MONGO_DBNAME][cls._collection].find(
            _filter, sort=[("_id", pymongo.DESCENDING)]
        ))
        objs = []
        for result in _results:
            obj = cls.dict_to_obj(result)
            objs.append(obj)
        return objs

    @classmethod
    def find_all(cls, _filter: dict = {}, limit: int = 1440):
        _results = list(cls._client[settings.MONGO_DBNAME][cls._collection].find(
            _filter, sort=[("_id", pymongo.DESCENDING)]
        ).limit(limit))
        objs = []
        for result in _results:
            obj = cls.dict_to_obj(result)
            objs.append(obj)
        return objs

    @classmethod
    def delete_all(cls, _filter: dict):
        return cls._client[settings.MONGO_DBNAME][cls._collection].delete_many(_filter)

    @classmethod
    def find_all_raw(cls, _filter: dict, limit: int = 1440):
        return list(cls._client[settings.MONGO_DBNAME][cls._collection].find(
            _filter, sort=[("_id", pymongo.DESCENDING)]
        ).limit(limit))

    @classmethod
    def find_all_raw_unlimited(cls, _filter: dict):
        return list(cls._client[settings.MONGO_DBNAME][cls._collection].find(
            _filter, sort=[("_id", pymongo.DESCENDING)]
        ))


class FieldValidationException(Exception):
    pass


class Field:

    def __init__(self, name, obj_type, is_list=False, validator=None, enums=None, is_required=False):
        """

        @rtype: object
        """
        self.name = name
        self.obj_type = obj_type
        self.is_list = is_list
        self.validator = validator
        self.enums = enums
        self.is_required = is_required

    def validate(self, value):
        self.validate_is_required(value) \
            .validate_enums(value) \
            .validate_obj_type(value)

    def try_cast(self, value):
        try:
            if type(value) == str and self.obj_type == datetime:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            else:
                return self.obj_type(value)
        except Exception:
            return value

    def validate_is_required(self, value):
        if self.obj_type is not float and self.obj_type is not int and self.obj_type is not bool and not value and self.is_required:
            raise FieldValidationException("{} is a required field".format(self.name))
        elif self.obj_type is int and value is None and self.is_required:
            raise FieldValidationException("{} is a required field".format(self.name))
        elif self.obj_type is float and value is None and self.is_required:
            raise FieldValidationException("{} is a required field".format(self.name))
        elif self.obj_type is bool and value is None and self.is_required:
            raise FieldValidationException("{} is a required field".format(self.name))
        return self

    def validate_obj_type(self, value):
        if value and type(value) != list:
            if type(value) != self.obj_type:
                raise FieldValidationException(
                    "{} has {} type while it should be {} type".format(self.name, type(value),
                                                                       self.obj_type))
        return self

    def validate_enums(self, value):
        if value:
            if self.enums:
                if value not in self.enums:
                    raise FieldValidationException(
                        "{} has {} value but only the following fields {} are allowed".format(self.name, value,
                                                                                              ",".join(self.enums)))
        return self

    def validate_is_list(self, value):
        if value:
            if type(value) != list and self.is_list:
                if value not in self.enums:
                    raise FieldValidationException(
                        "{} has {} type while it should be {} type".format(self.name, type(value),
                                                                           self.obj_type))
            if self.is_list:
                for item in value:
                    self.validate_obj_type(item)
        return self
