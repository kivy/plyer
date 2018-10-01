'''
Compatibility module for Python 2.7 and > 3.3
=============================================
'''
# pylint: disable=invalid-name

__all__ = ('PY2', 'string_types', 'queue', 'iterkeys',
           'itervalues', 'iteritems', 'xrange')

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
    string_types = basestring
    text_type = unicode
else:
    string_types = text_type = str

if PY2:
    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()
else:
    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

if PY2:
    # pylint: disable=undefined-variable
    # built-in actually, so it is defined in globals() for py2
    xrange = xrange
else:
    xrange = range
