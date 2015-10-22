from __future__ import absolute_import

import csv
import codecs
from cStringIO import StringIO

from restart.renderers import Renderer


class UnicodeCSVWriter(object):
    """A CSV writer that can write Unicode rows to the CSV file,
    which is encoded in the given encoding.

    According to https://docs.python.org/2/library/csv.html::
        The standard version of the `csv` module does not
        support Unicode input.

    Borrowed from https://docs.python.org/2/library/csv.html#examples.
    """
    def __init__(self, csvfile, dialect=csv.excel,
                 encoding='utf-8', **kwargs):
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwargs)
        self.stream = csvfile
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode('utf-8') for s in row])

        # Fetch utf-8 output from the queue
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        # And reencode it into the target encoding
        data = self.encoder.encode(data)

        # Write to the target stream
        self.stream.write(data)

        # Empty the queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.write(row)


class CSVRenderer(Renderer):
    """The CSV renderer class."""

    #: A tuple that specifies the columns in the CSV.
    #:
    #: Each item of `columns` is also a tuple in the form of
    #: `(header, fieldname)` or `(header, fieldname, converter)`.
    #:
    #: - header: The column header.
    #: - fieldname: The name of the field in the database, which
    #:              provides the original column value. To represent
    #:              a nested field, use dot (`.`) in its name.
    #: - converter: The converter used to make the final column value.
    #:
    #: The converter is determined in the following order:
    #:
    #:     1. The converter defined in the 3-tuple. Any function with
    #:        the following prototype can be specified as a converter
    #:        in the form of 3-tuple:
    #:
    #:         def converter(value):
    #:             return converted_value
    #:
    #:     2. The converter defined as a method, which has the following
    #:        prototype:
    #:
    #:         def convert_<fieldname>(self, value):
    #:             return converted_value
    #:
    #:        Note that the `fieldname` part is the column fieldname with
    #:        all its dots (`.`) transformed to underscores (`_`).
    #:
    #:     3. If not specified, use the default converter (`unicode`).
    #:
    #: For example:
    #:
    #:     def capitalize(value):
    #:         return value.capitalize()
    #:
    #:     class UserCSVRenderer(CSVRenderer):
    #:
    #:         columns = (
    #:             # A simple fieldname with the function-style converter
    #:             ('name', 'username', capitalize),
    #:             # A simple fieldname with the default converter
    #:             ('age', 'age'),
    #:             # A nested fieldname with the method-style converter
    #:             ('phone', 'contact.phone'),
    #:             ...
    #:         )
    #:
    #:         def convert_contact_phone(self, value):
    #:             return unicode('086-%s' % value)
    columns = None

    #: The default value for the missing field specified in the `columns`
    default_value = ''

    #: The content type bound to this renderer.
    content_type = 'text/csv'

    #: The format suffix bound to this renderer.
    format_suffix = 'csv'

    def render(self, data):
        """Render `data` into CSV.

        :param data: the data to be rendered.
        """
        assert isinstance(self.columns, tuple), \
            'The `columns` attribute must be a tuple object'
        assert isinstance(data, (dict, list, tuple)), \
            'The `data` argument must be a dict or a list or a tuple'

        # Assure that data is a sequence
        if isinstance(data, dict):
            data = [data]

        csv_file = StringIO()
        csv_writer = UnicodeCSVWriter(csv_file)

        # Write headers
        headers = [column[0] for column in self.columns]
        csv_writer.writerow(headers)

        # Write rows
        for each in data:
            values = []

            # Extract values
            for column in self.columns:
                if len(column) == 2:
                    _, fieldname = column
                    methodname = 'convert_%s' % fieldname.replace('.', '_')
                    converter = getattr(self, methodname, unicode)
                else:
                    _, fieldname, converter = column

                keys = fieldname.split('.')

                # Get the value of `fieldname` from `each`
                value = each
                for key in keys:
                    value = value.get(key)
                    if value is None:
                        value = self.default_value
                        break

                # Convert the value
                value = converter(value)

                values.append(value)

            # Write values
            csv_writer.writerow(values)

        csv_data = csv_file.getvalue()
        return csv_data
