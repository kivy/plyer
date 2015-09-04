from kivy.app import App
from plyer import camera
from plyer import gallery
from kivy.lang import Builder
from os.path import join, exists

tmpfileindex = 1


class MediaApp(App):
    '''This is a demo app meant for showcasing the usage of
    camera and gallery from within a kivy app.
    '''

    def build(self):
        return Builder.load_string('''
FloatLayout
    Image
        id: img
        size_hint: None, None
        size: root.size
        allow_stretch: True
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: None, None
        size: dp(300), dp(150)
        spacing: dp(9)
        Button
            text: 'Take Picture'
            on_release: app.take_picture()
        Button
            text: 'Choose from Gallery'
            on_release: app.choose_from_gallery()
''')

    def clear_tmpfiles(self):
        tmpdir = self.get_temporary_dir()
        for fn in os.listdir(tmpdir):
            if fn.startswith('Plyer-Photo-'):
                try:
                    os.unlink(join(tmpdir, fn))
                except:
                    pass

    def create_temporary_file(self):
        global tmpfileindex
        tmpdir = self.get_temporary_dir()
        while True:
            fn = join(tmpdir, 'Plyer-Photo-{}.jpg'.format(tmpfileindex))
            if not exists(fn):
                return fn
            tmpfileindex += 1

    def get_temporary_dir(self):
        return App.get_running_app().user_data_dir

    def take_picture(self):
        camera.take_picture(
            self.create_temporary_file(),
            self._on_picture_complete)

    def _on_picture_complete(self, fn):
        self.root.ids.img.source = fn

    def choose_from_gallery(self):
        #Gallery
        gallery.choose_image(
            self.create_temporary_file(),
            on_complete=self._on_gallery_chooser_complete)

    def _on_gallery_chooser_complete(self, fn, finished=False):
        # finished called when the user chooses cancel
        # with no file being selected
        if not finished:
            self.root.ids.img.source = fn


if __name__ == '__main__':
    MediaApp().run()
