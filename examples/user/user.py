from __future__ import absolute_import

from restart.api import RESTArt
from restart.ext.mongo.collection import Collection
from pymongo import MongoClient

api = RESTArt()


@api.register
class User(Collection):
    name = 'users'

    database = MongoClient().test
    collection_name = 'user'
