import os.path
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from plyer import camera

Builder.load_string('''
<CameraInterface>:
    orientation: 'vertical'

    Image:
        id: image
        source: None

    Button:
        text: "Take picture"
        size_hint_y: None
        height: "35sp"
        on_press: root.take_picture()
''')


class CameraInterface(BoxLayout):

    def take_picture(self):
        filename = os.path.join(app.user_data_dir, 'tmp.jpg')
        camera.take_picture(filename, self.on_picture)

    def on_picture(self, filename):
        self.ids.image.source = filename
        self.ids.image.reload()


class CameraApp(App):

    def build(self):
        return CameraInterface()

if __name__ == "__main__":
    app = CameraApp()
    app.run()
