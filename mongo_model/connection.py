# -*- coding: utf-8 -*-


import logging
from flask import current_app as app
from pymongo import MongoClient
from pymongo.database import Database
from mongomock import MongoClient as MockMongoClient, Database as MockDatabase


app_conn = {}   # Map apps to connections
logger = logging.getLogger(__name__)


class DBClient(object):
    @classmethod
    def init_conn(cls):
        try:
            db_name = app.config["MONGODB_SETTINGS"].pop('db_name')
            if app.testing:
                mongo_client = MockMongoClient
                db_class = MockDatabase
            else:
                mongo_client = MongoClient
                db_class = Database
            app_conn[app] = db_class(mongo_client(**app.config["MONGODB_SETTINGS"]), db_name)
        except KeyError:
            logger.error('Current app has not set configurations for MongoDB!')

    @classmethod
    def _get_connection(cls):
        try:
            return app_conn[app]
        except KeyError:
            DBClient.init_conn()
            return app_conn[app]

    def __getattr__(self, item):
        return self._get_connection().__getattr__(item)

    def __getitem__(self, item):
        return self._get_connection().__getitem__(item)

conn = DBClient()
