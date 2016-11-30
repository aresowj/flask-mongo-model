import unittest
import logging
from flask import Flask
from datetime import datetime
from mongo_model import ModelBase
from mongo_model.fields import StringField, DateTimeField


logger = logging.getLogger(__name__)


class TestModel(ModelBase):
    _collection_name = 'Test'
    _pk_name = '_id'

    field1 = StringField()

    def __init__(self):
        super(TestModel, self).__init__()
        self._add_field('field1')
        self.test_date = datetime.utcnow()
        self._add_field('datetime1', value=self.test_date)
        self._add_field('_id')


class MongoModelTest(unittest.TestCase):
    def test_init(self):
        instance = TestModel()
        # Initiate _fields from None to {}
        self.assertIsNotNone(instance._fields)

    def test_to_dict_non_json(self):
        instance = TestModel()
        d = instance.to_dict()
        self.assertIn('field1', d)
        self.assertIn('datetime1', d)
        self.assertIsInstance(d['datetime1'], datetime)
        # Should ignore Mongo object _id
        self.assertNotIn('_id', instance.to_dict())

    def test_to_dict_for_json(self):
        instance = TestModel()
        d = instance.to_dict(for_json=True)
        self.assertIn('field1', d)
        self.assertIn('datetime1', d)
        self.assertIsInstance(d['datetime1'], str)
        self.assertEqual(d['datetime1'], instance.test_date.isoformat())
        # Should ignore Mongo object _id
        self.assertNotIn('_id', d)

    def test_get(self):
        app = Flask(__name__)
        app.config['MONGODB_SETTINGS'] = {
            'host': '127.0.0.1',
            'port': 27017,
            'document_class': dict,
            'tz_aware': False,
            'connect': True,
            'db_name': __name__,
        }

        with app.app_context():
            instance = TestModel()
            instance.field1 = 'test'
            instance.save()

            logger.info(TestModel.get(field1='test'))
