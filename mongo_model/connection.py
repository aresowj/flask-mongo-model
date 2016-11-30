# -*- coding: utf-8 -*-


import logging
from pymongo import MongoClient
from pymongo.database import Database
from flask import current_app as app


app_conn = {}   # Map apps to connections
logger = None


class DBClient(object):
    @classmethod
    def init_conn(cls):
        try:
            db_name = app.config["MONGODB_SETTINGS"].pop('db_name')
            app_conn[app] = Database(MongoClient(**app.config["MONGODB_SETTINGS"]), db_name)
        except KeyError as e:
            logger.error('Current app has not set configurations for MongoDB!')

    @classmethod
    def _get_connection(cls):
        if app not in app_conn:
            global logger
            logger = logging.getLogger(app.logger_name)

            DBClient.init_conn()

        return app_conn[app]

    def __getattr__(self, item):
        return self._get_connection().__getattr__(item)

    def __getitem__(self, item):
        return self._get_connection().__getitem__(item)

conn = DBClient()
