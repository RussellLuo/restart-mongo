# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest

from restart.ext.mongo.ext.renderers import CSVRenderer


def capitalize(value, context):
    return value.capitalize()


class UserCSVRenderer(CSVRenderer):
    columns = (
        ('name', 'name', capitalize),
        ('age', 'age'),
        ('phone', 'contact.phone'),
        ('missing', 'missing'),
    )

    def convert_contact_phone(self, value, context):
        return unicode('086-%s' % value)


class UnicodeUserCSVRenderer(CSVRenderer):
    columns = (
        (u'名字', 'name', capitalize),
        (u'年龄', 'age'),
        (u'电话', 'contact.phone'),
        (u'缺失', 'missing'),
    )

    def convert_contact_phone(self, value, context):
        return unicode('086-%s' % value)


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

    def test_user_csv_renderer_with_invalid_data(self):
        renderer = UserCSVRenderer()

        with pytest.raises(AssertionError) as exc:
            renderer.render('')

        assert str(exc.value) == ('The `data` argument must be a dict or '
                                  'a list or a tuple')

    def test_user_csv_renderer_with_dict_data(self):
        renderer = UserCSVRenderer()
        rendered = renderer.render(self.data)
        assert rendered == ('name,age,phone,missing\r\n'
                            'Russell,8,086-123456,\r\n')

    def test_user_csv_renderer_with_list_data(self):
        renderer = UserCSVRenderer()
        rendered = renderer.render([self.data])
        assert rendered == ('name,age,phone,missing\r\n'
                            'Russell,8,086-123456,\r\n')

    def test_user_csv_renderer_with_tuple_data(self):
        renderer = UserCSVRenderer()
        rendered = renderer.render((self.data,))
        assert rendered == ('name,age,phone,missing\r\n'
                            'Russell,8,086-123456,\r\n')

    def test_unicode_user_csv_renderer_with_dict_data(self):
        renderer = UnicodeUserCSVRenderer()
        rendered = renderer.render(self.data)
        assert rendered.decode('utf-8') == (u'名字,年龄,电话,缺失\r\n'
                                             'Russell,8,086-123456,\r\n')
