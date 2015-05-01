from recycleview import RecycleView
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.app import App
from kivy.metrics import sp
import random
 
Builder.load_string("""
<Separator@Widget>:
    canvas.before:
        Color:
            rgb: (.5, .5, .5)
        Rectangle:
            pos: self.pos
            size: self.size

<LogItem@BoxLayout>:
    index: 0
    spacing: "5dp"
    contact_name: ""
    canvas.before:
        Color:
            rgb: (0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "14sp"
        text: root.contact_name
        color: (0, 1, 0, 1)
        text_size: (self.width, None)
""")
 
class TestApp(App):

    contacts = ListProperty()
    rv = RecycleView()

    def add_(self):

        names = ["Robert", "George", "Joseph", "Donald", "Mark", "Anthony", "Gary"]

        def callback(dt):
            self.rv.data.append({
                "viewclass": "LogItem",
                "contact_name": "{} {}".format(
                    random.choice(names),
                    random.choice(names)
                )
            })
            self.rv.refresh_from_data(force=True)
        Clock.schedule_interval(callback, 1 / 10.)



    def build(self):
        # Create a data set
        names = ["Robert", "George", "Joseph", "Donald", "Mark", "Anthony", "Gary"]

        for x in range(10):
            if x % 5 == 0:
                self.contacts.append({
                    "viewclass": "Separator",
                    "height": sp(20)
                })
            self.contacts.append({
                "index": x,
                "viewclass": "LogItem",
                "contact_name": "{} {}".format(
                    random.choice(names),
                    random.choice(names)
                )
            })

        self.rv.key_viewclass = "viewclass"
        self.rv.key_height = "height"
        self.rv.data = self.contacts
        self.add_()
        return self.rv

TestApp().run()
