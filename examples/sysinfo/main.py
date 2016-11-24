from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from plyer import sysinfo
from kivy.properties import StringProperty, ListProperty
from kivy.logger import Logger

Builder.load_string('''
<SysinfoInterface>:
    GridLayout:
        cols: 2
        Label:
            text: "Model"
        Label:
            text: root.model_
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
            text_size: self.size
            halign: "center"
            valign: "middle"
        Label:
            text: "Version"
        Label:
            text: root.version_
        Label:
            text: "Architecture"
        Label:
            text: root.architecture_
        Label:
            text: "Device"
        Label:
            text: root.device_
        Label:
            text: "Manufacturer"
        Label:
            text: root.manufacturer_
        Label:
            text: "Kernel"
        Label:
            text: root.kernel_
        Label:
            text: "Storage"
        Label:
            text: root.storage_
        Label:
            text: "Memory"
        Label:
            text: root.memory_
        Label:
            text: "Screen"
        Label:
            text: str(root.screen_)

''')


class SysinfoInterface(BoxLayout):

    model_ = StringProperty()
    platform_ = StringProperty()
    system_ = StringProperty()
    processor_ = StringProperty()
    version_ = StringProperty()
    architecture_ = StringProperty()
    device_ = StringProperty()
    manufacturer_ = StringProperty()
    kernel_ = StringProperty()
    storage_ = StringProperty()
    screen_ = ListProperty()
    memory_ = StringProperty()

    def __init__(self, **kwargs):
        super(SysinfoInterface, self).__init__(**kwargs)

    def update(self):
        Logger.info('plyer: update sysinfo data')
        self.get_model()
        self.get_platform()
        self.get_system()
        self.get_processor()
        self.get_version()
        self.get_architecture()
        self.get_device_name()
        self.get_manufacturer()
        self.get_kernel_version()
        self.get_storage_info()
        self.get_memory_info()
        self.get_screen_resolution()

    def get_model(self):
        self.model_ = sysinfo.model_info()

    def get_platform(self):
        self.platform_ = sysinfo.platform_info()

    def get_system(self):
        self.system_ = sysinfo.system_name()

    def get_processor(self):
        self.processor_ = sysinfo.processor_info()
        print(self.processor_)

    def get_version(self):
        temp = sysinfo.version_info()
        if type(temp) in (tuple, list):
            self.version_ = "{} {} {}".format(temp[0], temp[1], temp[2])
        else:
            self.version_ = temp
            
    def get_architecture(self):
        self.architecture_ = str(sysinfo.architecture_info())

    def get_device_name(self):
        self.device_ = sysinfo.device_name()

    def get_manufacturer(self):
        self.manufacturer_ = sysinfo.manufacturer_name()

    def get_kernel_version(self):
        self.kernel_ = sysinfo.kernel_version()

    def get_storage_info(self):
        free_bytes = sysinfo.storage_info()
        if free_bytes > 1073741824:  # 1GB
            self.storage_ = "{0:.2f} GB".format(free_bytes / 1024.0**3)
        else:
            self.storage_ = "{0} MB".format(free_bytes / 1024**2)

    def get_memory_info(self):
        try:
            self.memory_ = "{0:.2f} GB".format(sysinfo.memory_info() / 1024.0**3)
        except NotImplementedError:
            self.memory_ = '<Not Implemented>'

    def get_screen_resolution(self):
        self.screen_ = sysinfo.screen_resolution()


class SysinfoApp(App):

    def build(self):
        return SysinfoInterface()

    def on_start(self):
        self.root.update()

if __name__ == "__main__":
    app = SysinfoApp()
    app.run()
