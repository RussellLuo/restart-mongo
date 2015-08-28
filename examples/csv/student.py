# -*- coding: utf-8 -*-

from __future__ import absolute_import

from restart.api import RESTArt
from restart.renderers import JSONRenderer
from restart.ext.mongo.collection import Collection
from restart.ext.mongo.ext.renderers import CSVRenderer
from pymongo import MongoClient

api = RESTArt()


class StudentCSVRenderer(CSVRenderer):
    columns = (
        (u'姓名', 'name', unicode),
        (u'科目', 'course', unicode),
        (u'成绩', 'score', unicode),
    )


@api.route(uri='/students', endpoint='students_list', methods=['GET'],
           actions={'GET': 'index'}, format_suffix='optional')
@api.route(uri='/students/<pk>', endpoint='students_item', methods=['GET'],
           format_suffix='optional')
class Student(Collection):
    name = 'students'

    database = MongoClient().test
    collection_name = 'student'

    renderer_classes = (JSONRenderer, StudentCSVRenderer)
