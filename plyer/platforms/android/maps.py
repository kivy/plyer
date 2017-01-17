from jnius import cast
from jnius import autoclass
from plyer.facades.maps import Maps

PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')


class AndroidMaps(Maps):

    def _locate(self, **kwargs):
        lc = kwargs.get('lc')
        mapintent = Intent()
        mapintent.setAction(Intent.ACTION_VIEW)
        mapintent.setData(Uri.parse("geo:0,0?q="+lc))
        currActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currActivity.startActivity(mapintent)


def instance():
    return AndroidMaps()
