from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from plyer import sysinfo
from kivy.properties import StringProperty


Builder.load_string('''
<SysinfoInterface>:
    GridLayout:
        cols: 2
        Label:
            text: "Platform"
        Label:
            text: root.platform_
        Label:
            text: "System"
        Label:
            text: root.system_
        Label:
            text: "Processor"
        Label:
            text: root.processor_
        Label:
            text: "Distribution"
        Label:
            text: root.dist_


''')


class SysinfoInterface(BoxLayout):

    platform_ = StringProperty()
    system_ = StringProperty()
    processor_ = StringProperty()
    dist_ = StringProperty()

    def __init__(self, **kwargs):
        super(SysinfoInterface, self).__init__(**kwargs)
        self.update()

    def update(self):
        self.get_platform()
        self.get_system()
        self.get_processor()
        self.get_dist()

    def get_platform(self):
        self.platform_ = sysinfo.platform_info()

    def get_system(self):
        self.system_ = sysinfo.system_info()

    def get_processor(self):
        self.processor_ = sysinfo.processor_info()

    def get_dist(self):
        temp = sysinfo.dist_info()
        self.dist_ = "{} {} {}".format(temp[0], temp[1], temp[2])


class SysinfoApp(App):

    def build(self):
        return SysinfoInterface()

if __name__ == "__main__":
    app = SysinfoApp()
    app.run()
