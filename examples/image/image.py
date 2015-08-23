from __future__ import absolute_import

from restart.api import RESTArt
from restart.ext.mongo.file import File
from pymongo import MongoClient

api = RESTArt()


def make_tempdir():
    import tempfile
    tempdir = tempfile.mkdtemp()
    print('Directory `%s` is created for storing uploaded files. '
          'Remember to remove it by hand:-)' % tempdir)
    return tempdir


@api.register
class Image(File):
    name = 'images'

    upload_folder = make_tempdir()
    allowed_extensions = ('png', 'jpg', 'jpeg', 'gif')

    database = MongoClient().test
    collection_name = 'image'
