from __future__ import absolute_import

import json
from datetime import datetime

import bson
from restart.ext.mongo.collection import Collection
from restart.config import config
from restart.testing import RequestFactory
from mongomock import MongoClient


factory = RequestFactory()

db = MongoClient().test


class User(Collection):
    name = 'users'

    database = db
    collection_name = 'user'


class TestCollection(object):

    def make_resource(self, **actions):
        action_map = config.ACTION_MAP.copy()
        if actions:
            action_map.update(actions)
        return User(action_map)

    def create_user(self, name='russell'):
        data = {
            'name': name,
            'password': '123456',
            'date_joined': 'datetime(2015-08-14T00:00:00Z)'
        }
        request = factory.post('/users', data=json.dumps(data),
                               content_type='application/json')
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        # Convert the response string (JSON) to a dict
        response.data = json.loads(response.data)

        return response

    def test_index(self):
        request = factory.get('/users')
        resource = self.make_resource(GET='index')
        response = resource.dispatch_request(request)

        # Assert the response
        assert response.data == '[]'
        assert response.status_code == 200

    def test_create(self):
        response = self.create_user()

        # Assert the response
        assert '_id' in response.data
        _id = response.data['_id']
        assert response.headers['Location'].endswith('/users/%s' % _id)
        assert response.status_code == 201

        # Assert the database
        user = db.user.find_one({'_id': bson.ObjectId(_id)})
        assert user is not None
        assert user['name'] == 'russell'
        assert user['password'] == '123456'
        assert user['date_joined'] == datetime(2015, 8, 14)

    def test_read(self):
        response = self.create_user()
        _id = response.data['_id']

        request = factory.get('/users/%s' % _id)
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        resp_data = json.loads(response.data)
        assert resp_data['_id'] == _id
        assert resp_data['name'] == 'russell'
        assert resp_data['password'] == '123456'
        assert resp_data['date_joined'] == '2015-08-14T00:00:00Z'
        assert response.status_code == 200

    def test_replace(self):
        response = self.create_user()
        _id = response.data['_id']

        data = {
            'name': 'tracey',
            'password': '123456',
            'date_joined': 'datetime(2015-08-14T00:00:00Z)'
        }
        request = factory.put('/users/%s' % _id, data=json.dumps(data),
                              content_type='application/json')
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        assert response.data == '""'
        assert response.status_code == 204

        # Assert the database
        user = db.user.find_one({'_id': bson.ObjectId(_id)})
        assert user is not None
        assert user['name'] == 'tracey'
        assert user['password'] == '123456'
        assert user['date_joined'] == datetime(2015, 8, 14)

    def test_update(self):
        response = self.create_user()
        _id = response.data['_id']

        data = [{
            'op': 'add',
            'path': '/password',
            'value': '666666'
        }]
        request = factory.patch('/users/%s' % _id, data=json.dumps(data),
                                content_type='application/json')
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        assert response.data == '""'
        assert response.status_code == 204

        # Assert the database
        user = db.user.find_one({'_id': bson.ObjectId(_id)})
        assert user is not None
        assert user['name'] == 'russell'
        assert user['password'] == '666666'
        assert user['date_joined'] == datetime(2015, 8, 14)

    def test_delete(self):
        response = self.create_user()
        _id = response.data['_id']

        request = factory.delete('/users/%s' % _id)
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        assert response.data == '""'
        assert response.status_code == 204

        # Assert the database
        user = db.user.find_one({'_id': bson.ObjectId(_id)})
        assert user is None
