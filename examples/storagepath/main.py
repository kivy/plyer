'''
Storage Path Example.
'''

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
#: import storagepath plyer.storagepath
<StoragePathInterface>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            Button:
                text: 'Home'
                on_press: label.text = str(storagepath.get_home_dir())
            Button:
                text: 'External Storage'
                on_press:
                    label.text = str(storagepath.get_external_storage_dir())
        BoxLayout:
            Button:
                text: 'Root'
                on_press: label.text = str(storagepath.get_root_dir())
            Button:
                text: 'Documents'
                on_press: label.text = str(storagepath.get_documents_dir())
        BoxLayout:
            Button:
                text: 'Downloads'
                on_press: label.text = str(storagepath.get_downloads_dir())
            Button:
                text: 'Videos'
                on_press: label.text = str(storagepath.get_videos_dir())
        BoxLayout:
            Button:
                text: 'Music'
                on_press: label.text = str(storagepath.get_music_dir())
            Button:
                text: 'Pictures'
                on_press: label.text = str(storagepath.get_pictures_dir())
        Button:
            text: 'Applications'
            on_press: label.text = str(storagepath.get_application_dir())
        Label:
            id: label
''')


class StoragePathInterface(BoxLayout):
    pass


class StoragePathApp(App):

    def build(self):
        return StoragePathInterface()


if __name__ == "__main__":
    StoragePathApp().run()
