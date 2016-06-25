from os import unlink
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from plyer.facades import Camera

Builder.load_string('''
<GenericCameraWidget>:
    orientation: 'vertical'
    canvas:
        Color:
            rgb: 0, 0, 0
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Plyer generic Camera"

    Camera:
        id: camera
        resolution: (640, 480)
        size_hint: 1, 1

    BoxLayout:
        Button:
            text: "Shoot"
            size_hint_y: None
            height: "35sp"
            on_press: root.shoot()
        Button:
            text: "Cancel"
            size_hint_y: None
            height: "35sp"
            on_press: root.close()
''')


class GenericCameraWidget(BoxLayout):
    filename = StringProperty()
    callback = ObjectProperty()

    def shoot(self):
        self.ids.camera.texture.save(self.filename, flipped=False)
        should_unlink = self.callback(self.filename)
        if should_unlink:
            try:
                unlink(self.filename)
            except:
                pass
        self.close()

    def close(self):
        app = App.get_running_app()
        self.ids.camera._camera.release()
        app.root_window.remove_widget(self)


class GenericCamera(Camera):
    widget = None

    def _take_picture(self, on_complete, filename=None):
        app = App.get_running_app()
        widget = GenericCameraWidget(callback=on_complete,
                                     filename=filename)
        app.root_window.add_widget(widget)


def instance():
    return GenericCamera()
