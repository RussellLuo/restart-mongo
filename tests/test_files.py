from __future__ import absolute_import

import os
import json
import shutil
import tempfile
from datetime import datetime
from cStringIO import StringIO

import bson
from restart.ext.mongo.ext.files import Files
from restart.config import config
from restart.testing import RequestFactory
from mongomock import MongoClient


factory = RequestFactory()
now = datetime.now()

tempdir = tempfile.mkdtemp()
db = MongoClient().test


class Images(Files):
    name = 'images'

    upload_folder = tempdir
    allowed_extensions = ('png', 'jpg', 'jpeg', 'gif')

    database = db
    collection_name = 'image'


class TestFiles(object):

    def setup_class(cls):
        cls.tempdir = tempdir

    def teardown_class(cls):
        shutil.rmtree(cls.tempdir)

    def make_resource(self, **actions):
        action_map = config.ACTION_MAP.copy()
        if actions:
            action_map.update(actions)
        return Images(action_map)

    def get_data(self, ext='.png', form_data=None):
        data = {'image': (StringIO('this is an image'), 'test%s' % ext)}
        if isinstance(form_data, dict):
            data.update(form_data)
        return data

    def create_image(self, ext='.png', form_data=None):
        request = factory.post('/images', data=self.get_data(ext, form_data))
        resource = self.make_resource()
        response = resource.dispatch_request(request)
        # Convert the response string (JSON) to a dict
        response.data = json.loads(response.data)
        return response

    def assert_exists(self, path, exists):
        filename = os.path.join(Images.upload_folder, path)
        assert os.path.isfile(filename) is exists

    def test_create_image(self):
        response = self.create_image()

        # Assert the response
        assert '_id' in response.data
        assert response.status_code == 201

        # Assert the database
        _id = bson.ObjectId(response.data['_id'])
        image = db.image.find_one({'_id': _id})
        assert image is not None
        assert image['initial_name'] == 'test.png'
        archive_name = now.strftime(Images.archive_name_format)
        assert image['storage_path'].startswith(archive_name)
        assert image['date_uploaded'].date() == now.date()

        # Assert the file system
        self.assert_exists(image['storage_path'], True)

    def test_create_image_with_form_data(self):
        form_data = {'extra_field': 'some value'}
        response = self.create_image(form_data=form_data)

        # Assert the response
        assert '_id' in response.data
        assert response.status_code == 201

        # Assert the database
        _id = bson.ObjectId(response.data['_id'])
        image = db.image.find_one({'_id': _id})
        assert image is not None
        assert image['initial_name'] == 'test.png'
        archive_name = now.strftime(Images.archive_name_format)
        assert image['storage_path'].startswith(archive_name)
        assert image['date_uploaded'].date() == now.date()
        assert image['extra_field'] == form_data['extra_field']

        # Assert the file system
        self.assert_exists(image['storage_path'], True)

    def test_create_image_with_disallowed_extension(self):
        response = self.create_image(ext='.txt')

        # Assert the response
        assert response.data == {
            'message': ('Only file extensions (png, jpg, jpeg, gif) '
                        'are allowed')
        }
        assert response.status_code == 400

    def test_replace_image(self):
        response = self.create_image()
        _id = response.data['_id']

        # Save the storage path for later use
        image = db.image.find_one({'_id': bson.ObjectId(_id)})
        storage_path = image['storage_path']

        request = factory.put('/images/%s' % _id,
                              data=self.get_data(ext='.jpg'))
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        assert response.data == '""'
        assert response.status_code == 204

        # Assert the database
        image = db.image.find_one({'_id': bson.ObjectId(_id)})
        assert image is not None
        assert image['initial_name'] == 'test.jpg'
        assert image['date_uploaded'].date() == now.date()

        # Assert the file system
        self.assert_exists(storage_path, False)
        self.assert_exists(image['storage_path'], True)

    def test_replace_image_with_form_data(self):
        form_data = {'extra_field': 'some value'}
        response = self.create_image(form_data=form_data)
        _id = response.data['_id']

        # Save the storage path for later use
        image = db.image.find_one({'_id': bson.ObjectId(_id)})
        storage_path = image['storage_path']

        new_form_data = {'extra_field': 'some new value'}
        request = factory.put('/images/%s' % _id,
                              data=self.get_data(ext='.jpg',
                                                 form_data=new_form_data))
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        assert response.data == '""'
        assert response.status_code == 204

        # Assert the database
        image = db.image.find_one({'_id': bson.ObjectId(_id)})
        assert image is not None
        assert image['initial_name'] == 'test.jpg'
        assert image['date_uploaded'].date() == now.date()
        assert image['extra_field'] == new_form_data['extra_field']

        # Assert the file system
        self.assert_exists(storage_path, False)
        self.assert_exists(image['storage_path'], True)

    def test_replace_image_while_using_old_storage_path(self):
        response = self.create_image()
        _id = response.data['_id']

        # Save the storage path for later use
        image = db.image.find_one({'_id': bson.ObjectId(_id)})
        storage_path = image['storage_path']

        request = factory.put('/images/%s' % _id,
                              data=self.get_data(ext='.jpg'),
                              headers=[('X-Keep-Storage-Path', 'true')])
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        assert response.data == '""'
        assert response.status_code == 204

        # Assert the database
        image = db.image.find_one({'_id': bson.ObjectId(_id)})
        assert image is not None
        assert image['initial_name'] == 'test.jpg'
        assert image['storage_path'] == storage_path
        assert image['date_uploaded'].date() == now.date()

        # Assert the file system
        self.assert_exists(storage_path, True)

    def test_update_image(self):
        response = self.create_image()
        _id = response.data['_id']

        request = factory.patch('/images/%s' % _id, data=self.get_data())
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        assert response.data == ('{"message": "The method is not allowed '
                                 'for the requested URL."}')
        assert response.status_code == 405

    def test_delete_image(self):
        response = self.create_image()
        _id = response.data['_id']

        # Save the storage path for later use
        image = db.image.find_one({'_id': bson.ObjectId(_id)})
        storage_path = image['storage_path']

        request = factory.delete('/images/%s' % _id, data=self.get_data())
        resource = self.make_resource()
        response = resource.dispatch_request(request, _id)

        # Assert the response
        assert response.data == '""'
        assert response.status_code == 204

        # Assert the database
        image = db.image.find_one({'_id': bson.ObjectId(_id)})
        assert image is None

        # Assert the file system
        self.assert_exists(storage_path, False)
