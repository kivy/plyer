from plyer.facades import Gallery
import jnius
from android import activity
from android import autoclass
import threading
from time import sleep

Intent = autoclass ('android.content.Intent')
PythonActivity = autoclass ('org.renpy.android.PythonActivity')
Uri = autoclass('android.net.Uri')
CompressFormat = autoclass('android.graphics.Bitmap$CompressFormat')
BitmapFactory = autoclass('android.graphics.BitmapFactory')
FileInputStream = autoclass('java.io.FileInputStream')
FileOutputStream = autoclass('java.io.FileOutputStream')
BufferedOutputStream = autoclass('java.io.BufferedOutputStream')
ContentResolver = PythonActivity.mActivity.getContentResolver()
Version = autoclass('android.os.Build$VERSION')

class AndroidGallery(Gallery):

    def _choose_image(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename

        activity.unbind(on_activity_result=self.on_activity_result)
        activity.bind(on_activity_result=self.on_activity_result)
        intent = Intent(Intent.ACTION_PICK)
        intent.setType("image/jpeg")
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, True)
        #intent.putExtra(Intent.EXTRA_LOCAL_ONLY, True)
        #intent.putExtra(Intent.CATEGORY_OPENABLE, True)
        PythonActivity.mActivity.startActivityForResult(
            Intent.createChooser(intent, autoclass(
                'java.lang.String')("Select Picture")), 0x100)

    def on_activity_result(self, requestCode, resultCode, intent):
        activity.unbind(on_activity_result=self.on_activity_result)

        if requestCode != 0x100:
	        return
        if resultCode != -1:
            self.on_complete([], True)
            return

        uri = []
        #data = intent.getData()
        #if data:
	        #self._get_path_from_URI([data])
        uri = []
        data = intent.getClipData()
        if not data:
            return
        for x in range(data.getItemCount()):
            item = data.getItemAt(x)
            urI = item.getUri()
            uri.append(urI)

        PythonActivity.toastError("Loading {} image/s".format(len(uri)))
        print 'calling get path form uri ', uri
        th = threading.Thread(target=self._get_path_from_URI, args=[uri])
        th.start()

    def _get_path_from_URI(self, uris):
        # return a list of all the uris converted to their paths
        ret = []
        for count, uri in enumerate(uris):
            scheme = uri.getScheme()
            if scheme == 'content':
                PythonActivity.toastError('Loading file {}'.format(count +  1))
                try:
                    cursor = ContentResolver.query(
                            uri, None, None, None, None)
                    if cursor.moveToFirst():
                        index = cursor.getColumnIndexOrThrow('_data')
                        uri = Uri.parse(cursor.getString(index))
                        pth = uri.getPath()
                        if pth:
                            ret.append(pth)
                except Exception as e:
                    parcelFileDescriptor = ContentResolver.openFileDescriptor(uri, 'r')
                    #ist = FileInputStream(parcelFileDescriptor.getFileDescriptor())
                    file_nm, ext = self.filename.rsplit('.')
                    filename = file_nm[:-1] + str(int(file_nm[-1]) + 1) + '.' + ext
                    self.filename = filename
                    #ln = 0
                    output = BufferedOutputStream(FileOutputStream(filename))
                    bitmap = BitmapFactory.decodeFileDescriptor(parcelFileDescriptor.getFileDescriptor())
                    bitmap.compress(CompressFormat.JPEG, 100, output)
                    ret.append(filename)
                    #ist.close()
                    continue
                except Exception as e:
                    Logger.debug('ScramPhoto: {}'.format(e))
                    continue
            elif scheme != 'file':
                continue
        self.on_complete(ret, False)
        #jnius.detach()
        sleep(2000000000)


def instance():
    return AndroidGallery()
