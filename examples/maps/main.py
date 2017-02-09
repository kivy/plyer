from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from plyer import maps

Builder.load_string('''
<MapsInterface>
    orientation: 'vertical'
    Label:
        text:"Welcome to Maps"
    TextInput:
        id: getlocation
        hint_text: "Enter Location"
        multiline: False
    GetLocationButton:
        lc: getlocation.text
        text: 'Go to location'
        on_release: self.findlocation()

''')


class MapsInterface(BoxLayout):
    pass


class GetLocationButton(Button):
    lc = StringProperty()

    def findlocation(self, *args):
        maps.locate(lc=self.lc)


class MapSampleApp(App):

    def build(self):
        return MapsInterface()

if __name__ == "__main__":
    MapSampleApp().run()
