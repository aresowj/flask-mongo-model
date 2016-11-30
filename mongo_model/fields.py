# -*- coding: utf-8 -*-


import logging


logger = logging.getLogger(__name__)


class MongoField(object):
    _value = None
    _nullable = True
    _default = None
    _mutable = True
    _primary_key = False
    _build_index = False
    _max_length = None

    def __init__(self, *args, **kwargs):
        for k, v in kwargs:
            name = '_' + k

            if hasattr(self, name):
                self.__setattr__(name, v)

    def set_value(self, val):
        self._value = val


class StringField(MongoField):
    _value = ''


class IntegerField(MongoField):
    pass


class FloatField(MongoField):
    pass


class TextField(MongoField):
    pass


class DateTimeField(MongoField):
    pass
