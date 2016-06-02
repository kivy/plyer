'''
Android Sharing
-----------
'''

from jnius import autoclass, cast
from plyer.facades import Sharing
from plyer.platforms.android import activity

Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
File = autoclass('java.io.File')
Arraylist = autoclass('java.util.ArrayList')
PythonActivity = autoclass('org.renpy.android.PythonActivity')


class AndroidSharing(Sharing):

    def _share_text(self, **kwargs):

        String = autoclass('java.lang.String')
        extra_text = kwargs.get('extra_text')
        extra_subject = kwargs.get('extra_subject')

        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_SUBJECT, cast('java.lang.CharSequence',
                        String(extra_subject)))
        intent.putExtra(Intent.EXTRA_TEXT, cast('java.lang.CharSequence',
                        String(extra_text)))
        intent.setType('text/plain')

        _Activity = cast('android.app.Activity', PythonActivity.mActivity)
        _Activity.startActivity(intent)

    def _share_images(self, **kwargs):

        images = kwargs.get('images')
        imageUris = Arraylist()
        for i in range(len(images)):
            photofile = File(images[i])
            uri = Uri.fromFile(photofile)
            imageUris.add(uri)
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND_MULTIPLE)
        intent.putParcelableArrayListExtra(Intent.EXTRA_STREAM, imageUris)
        intent.setType("image/*")

        _Activity = cast('android.app.Activity', PythonActivity.mActivity)
        _Activity.startActivity(intent)

    def _share_files(self, **kwargs):

        files = kwargs.get('files')
        filesUris = Arraylist()
        for i in range(len(files)):
            share_file = File(files[i])
            uri = Uri.fromFile(share_file)
            filesUris.add(uri)
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND_MULTIPLE)
        intent.putParcelableArrayListExtra(Intent.EXTRA_STREAM, filesUris)
        intent.setType("*/*")

        _Activity = cast('android.app.Activity', PythonActivity.mActivity)
        _Activity.startActivity(intent)


def instance():
    return AndroidSharing()
