from __future__ import absolute_import

import csv
from cStringIO import StringIO

from restart.renderers import Renderer


class CSVRenderer(Renderer):
    """The CSV renderer class."""

    #: A tuple that specifies the columns in the CSV.
    #: Each item of `columns` is also a tuple in the form
    #: `(header, fieldname, converter)`.
    #:
    #: For example:
    #:
    #:     def capitalize(value):
    #:         return value.capitalize()
    #:
    #:     columns = (
    #:         # A simple fieldname with a customized `capitalize` converter
    #:         ('name', 'username', capitalize),
    #:         # A simple fieldname without converter
    #:         ('age', 'age', None),
    #:         # A nested fieldname with the built-in `unicode` converter
    #:         ('phone', 'contact.phone', unicode),
    #:         ...
    #:     )
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
        assert isinstance(data, dict), \
            'The `data` argument must be a dict object'

        csv_file = StringIO()
        csv_writer = csv.writer(csv_file)

        # Write headers
        headers = [column[0] for column in self.columns]
        csv_writer.writerow(headers)

        # Extract values
        values = []
        for _, fieldname, converter in self.columns:
            keys = fieldname.split('.')

            # Get the value of `fieldname` from `data`
            value = data
            for key in keys:
                value = value.get(key)
                if value is None:
                    value = self.default_value
                    break

            # Convert the value if possible
            if converter is not None:
                value = converter(value)

            values.append(value)

        # Write values
        csv_writer.writerow(values)

        csv_data = csv_file.getvalue()
        return csv_data
