from __future__ import absolute_import


def get_exception_detail(e):
    if not isinstance(e, Exception):
        return u''
    return u'%s: %s' % (e.__class__.__name__, e.message)
