from kivy.app import App
from kivy.lang import Builder
from kivy.lib import osc
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

serviceport = 3001
activityport = 3002

Builder.load_string('''
<ServiceInterface>:
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            Button:
                text: 'ping!'
                on_press: app.ping()
            Label:
                text: app.serv_msg
        BoxLayout:
            Button:
                text: "stop service"
                on_press: app.stop_service()
            Button:
                text: 'start service'
                on_press: app.start_service()
''')


class ServiceInterface(BoxLayout):
    pass


class ServiceApp(App):

    serv_msg = StringProperty(':P')

    def build(self):
        self.start_service()

        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=activityport)
        # activity port
        osc.bind(oscid, self.api_callback, '/some_api')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0.3)

        return ServiceInterface()

    def start_service(self):
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('Pycon Service', 'running')
            service.start('service started')
            self.service = service

    def ping(self):
        self.serv_msg = ":D"
        osc.sendMsg('/some_api', ['ping'], port=serviceport)
        # service port

    def stop_service(self):
        if self.service:
            self.service.stop()
        self.service = None

    def api_callback(self, message, *args):
        self.serv_msg += ':::'
        self.serv_msg += '\n{}'.format(message[2])

if __name__ == '__main__':
    ServiceApp().run()
