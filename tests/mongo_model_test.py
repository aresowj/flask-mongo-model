import unittest
import logging
from datetime import datetime
from flask import Flask
from mongo_model import ModelBase
from mongo_model.fields import StringField, DateTimeField


logger = logging.getLogger(__name__)


class TestModel(ModelBase):
    _collection_name = 'Test'

    field1 = StringField()
    timestamp = DateTimeField()


class MongoModelTest(unittest.TestCase):
    def test_init(self):
        instance = TestModel()
        # Initiate _fields from None to a dictionary containing pairs
        # {name: field_instance}
        self.assertIsNotNone(instance._fields)

    def test_to_dict_non_json(self):
        instance = TestModel()
        d = instance.to_dict()
        self.assertIn('field1', d)
        self.assertIn('timestamp', d)
        self.assertIsInstance(d['timestamp'], datetime)
        # Should ignore Mongo object _id
        self.assertNotIn('_id', instance.to_dict())

    def test_to_dict_for_json(self):
        instance = TestModel()
        d = instance.to_dict(for_json=True)
        self.assertIn('field1', d)
        self.assertIn('timestamp', d)
        self.assertIsInstance(d['timestamp'], str)
        self.assertEqual(d['timestamp'], instance.timestamp.isoformat())
        # Should ignore Mongo object _id
        self.assertNotIn('_id', d)

    def test_get(self):
        app = Flask(__name__)
        app.testing = True

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
            self.assertIsInstance(super(ModelBase, instance).__getattribute__('field1'), StringField)
            instance.save()

            # Get with either field
            instance_from_db = TestModel.get(field1='test')
            self.assertEqual(instance_from_db.field1, instance.field1)
            self.assertEqual(instance_from_db.timestamp, instance.timestamp)

            instance_from_db = TestModel.get(timestamp=instance.timestamp)
            self.assertEqual(instance_from_db.field1, instance.field1)
            self.assertEqual(instance_from_db.timestamp, instance.timestamp)

            # Get with multiple fields
            instance_from_db = TestModel.get(field1='test', timestamp=instance.timestamp)
            self.assertEqual(instance_from_db.field1, instance.field1)
            self.assertEqual(instance_from_db.timestamp, instance.timestamp)
