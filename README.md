# RESTArt-Mongo

A RESTArt extension for using MongoDB.


Installation
------------

Install `RESTArt-Mongo` with `pip`:

    $ pip install RESTArt-Mongo

Install development version from `GitHub`:

    $ git clone https://github.com/RussellLuo/restart-mongo.git
    $ cd restart-mongo
    $ python setup.py install


Quickstart
----------

Here is a very simple `Users` resource, which is mapped to an `user` collection in local MongoDB:

    from restart.api import RESTArt
    from restart.ext.mongo.collection import Collection
    from pymongo import MongoClient

    api = RESTArt()

    @api.register
    class Users(Collection):
        name = 'users'

        database = MongoClient().test
        collection_name = 'user'

See [examples](examples) for more details.
