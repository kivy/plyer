'''
Toast
-----------
'''

from plyer.facades import Toast
from android.runnable import run_on_ui_thread
from jnius import autoclass, cast
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Context = autoclass('android.content.Context')


class AndroidToast(Toast):

    @run_on_ui_thread
    def _maketoast(self, **kwargs):
        Toast = autoclass("android.widget.Toast")
        String = autoclass('java.lang.String')
        text = kwargs.get('text')
        duration = int(kwargs.get('duration'))
        c = cast('java.lang.CharSequence', String(text))
        context = PythonActivity.mActivity.getApplicationContext()
        t = Toast.makeText(context, c, duration)
        t.show()
        return t


def instance():
    return AndroidToast()
