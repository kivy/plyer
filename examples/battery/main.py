from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from plyer import battery

Builder.load_string('''
<BatteryInterface>:
    lbl1: lbl1
    lbl2: lbl2
    FloatLayout:

        Button:
            size_hint_y: None
            pos_hint: {'y': .5}
            text: "Battery Status"
            on_press: root.get_status()
        BoxLayout:
            size_hint_y: None
            pos_hint: {'y': .1}
            Label:
                text: "Is Charging?"
            Label:
                id: lbl1
                text:
            Label:
                text: "Percentage"
            Label:
                id: lbl2
                text:

''')


class BatteryInterface(BoxLayout):
    lbl1 = ObjectProperty()
    lbl2 = ObjectProperty()

    def get_status(self, *args):
        self.lbl1.text = str(battery.status['isCharging'])
        self.lbl2.text = str(battery.status['percentage']) + "%"


class BatteryApp(App):

    def build(self):
        return BatteryInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    app = BatteryApp()
    app.run()
