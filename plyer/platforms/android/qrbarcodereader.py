from jnius import cast
from jnius import autoclass
from plyer.facades import QrBarcodeReader

PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')

class AndroidQrBarcodeReader(QrBarcodeReader):

    def _scan(self):

        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setData(Uri.parse('http://www.onlinebarcodereader.com'))

        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)

def instance():
    return AndroidQrBarcodeReader()
