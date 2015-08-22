from __future__ import absolute_import

import pytest

from restart.ext.mongo.renderers import CSVRenderer


def capitalize(value):
    return value.capitalize()


class UserCSVRenderer(CSVRenderer):
    columns = (
        ('name', 'name', capitalize),
        ('age', 'age', None),
        ('phone', 'contact.phone', unicode),
        ('missing', 'missing', unicode),
    )


class TestRenderers(object):

    data = {
        'name': 'russell',
        'age': 8,
        'contact': {
            'phone': '123456'
        }
    }

    def test_csv_renderer(self):
        renderer = CSVRenderer()

        with pytest.raises(AssertionError) as exc:
            renderer.render(self.data)

        expected_exc_msg = 'The `columns` attribute must be a tuple object'
        assert str(exc.value) == expected_exc_msg

    def test_user_csv_renderer_with_non_dict_data(self):
        renderer = UserCSVRenderer()

        with pytest.raises(AssertionError) as exc:
            renderer.render('')

        expected_exc_msg = 'The `data` argument must be a dict object'
        assert str(exc.value) == expected_exc_msg

    def test_user_csv_renderer_with_dict_data(self):
        renderer = UserCSVRenderer()
        rendered = renderer.render(self.data)
        assert rendered == ('name,age,phone,missing\r\n'
                            'Russell,8,123456,\r\n')
