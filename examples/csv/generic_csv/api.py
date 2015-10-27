from __future__ import absolute_import

from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import BadRequest
from restart.ext.mongo.collection import Collection
from restart.ext.mongo.ext.dufilter import DuFilter
from restart.ext.mongo.ext.renderers import CSVRenderer
from pymongo import MongoClient

api = RESTArt()
cli = MongoClient()


class DynamicCollection(Collection):
    """Collection with dynamic database and collection-name."""

    filter_class = DuFilter

    def __init__(self, database, collection_name, *args, **kwargs):
        """Override to set database and collection_name."""
        self.database = database
        self.collection_name = collection_name
        super(DynamicCollection, self).__init__(*args, **kwargs)


class DynamicCSVRenderer(CSVRenderer):
    """CSVRenderer with dynamic columns."""

    def render(self, data):
        """Override to split columns out of data."""
        # An unknown CSV (by default)
        self.columns = (('unknown', 'unknown'),)
        actual_data = {'unknown': unicode(data)}

        if isinstance(data, dict):
            keys = data.keys()
            # The normal CSV (everything is ok)
            if sorted(keys) == ['columns', 'data']:
                self.columns = data['columns']
                actual_data = data['data']
            # The exception CSV (if some exception occurs)
            elif keys == ['message']:
                self.columns = (('message', 'message'),)
                actual_data = data

        return super(DynamicCSVRenderer, self).render(actual_data)


@api.register(format_suffix='mandatory')
class GenericCSV(Resource):
    name = 'generic-csvs'

    renderer_classes = (DynamicCSVRenderer,)

    allowed_databases = {
        'test': cli.test
    }

    def get_csv_args(self, request):
        database_name = request.args.pop('database', None)
        if database_name not in self.allowed_databases:
            raise BadRequest(
                'The database %r is not allowed' % database_name
            )
        database = self.allowed_databases[database_name]

        collection_name = request.args.pop('collection_name', None)
        if collection_name is None:
            raise BadRequest('The `collection_name` must be specified')

        fields = request.args.get('fields')
        if fields is None:
            raise BadRequest('The `fields` to be exported must be specified')
        columns = [(field, field) for field in fields.split(',')]

        return database, collection_name, tuple(columns)

    def index(self, request):
        database, collection_name, columns = self.get_csv_args(request)
        resource = DynamicCollection(database, collection_name,
                                     action_map={'GET': 'index'})
        resource.request = request
        rv = resource.perform_action()
        response = resource.make_response(rv)

        response.data = {
            'columns': columns,
            'data': response.data,
        }
        return response
