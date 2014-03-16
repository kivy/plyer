from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from os import unlink

Builder.load_string('''
<GUI>:
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: camera
            resolution: (640, 480)
            play: True
        Button:
            id: capturebtn
            text: 'Capture'
            size_hint_y: None
            height: '48dp'
''')

class GUI(BoxLayout):
    pass
        
class CaptureCamera(App):
    def __init__(self, on_complete, filename):
        super(CaptureCamera, self).__init__()
        self.filename = filename
        self.on_complete = on_complete

    def on_stop(self):
        if(self.on_complete(self.filename)):
            self._unlink(self.filename)

    def _unlink(self, fn):
        try:
            unlink(fn)
        except:
            pass

    def _save_picture(self, obj):
        camera = self.gui.ids.camera
        
        img = Image(camera.texture)
        img.save(self.filename)
        camera.play = False
        
        self.stop()

    def build(self):
        self.gui = GUI()
        self.gui.ids.capturebtn.bind(on_release=self._save_picture)
        return self.gui

class OSXCamera():
    capture = None
    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        assert(filename is not None)

        self.capture = CaptureCamera(on_complete, filename) 
        self.capture.run()

def instance():
    return OSXCamera()
    