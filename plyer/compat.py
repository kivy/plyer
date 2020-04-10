'''
Compatibility module for Python 2.7 and > 3.3
=============================================
'''
# pylint: disable=invalid-name

__all__ = ('PY2', 'string_types', 'queue', 'iterkeys',
           'itervalues', 'iteritems')

import sys
try:
    import queue
except ImportError:
    import Queue as queue

#: True if Python 2 intepreter is used
PY2 = sys.version_info[0] == 2

#: String types that can be used for checking if a object is a string
string_types = None
text_type = None
if PY2:
    # pylint: disable=undefined-variable
    # built-in actually, so it is defined in globals() for py2
    string_types = basestring  # noqa F821 undefined name 'basestring'
    text_type = unicode  # noqa F821 undefined name 'unicode'
else:
    string_types = text_type = str

if PY2:
    def iterkeys(d): return d.iterkeys()
    def itervalues(d): return d.itervalues()
    def iteritems(d): return d.iteritems()
else:
    def iterkeys(d): return iter(d.keys())
    def itervalues(d): return iter(d.values())
    def iteritems(d): return iter(d.items())
