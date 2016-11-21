from kivy.app import App
from kivy.lang import Builder
from kivy.lib import osc
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from os.path import dirname
from os.path import join
from os.path import realpath

from plyer import notification
from plyer.utils import platform
from plyer.compat import PY2

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

    def speak(self):
        osc.sendMsg('/some_api', ['speak'], port=serviceport)

    def do_notify(self, mode='normal'):
        title = "Pycon India"
        message = "Talk in 10 minutes"
        if PY2:
            title = title.decode('utf8')
            message = message.decode('utf8')
        

        if mode == 'fancy':
            kwargs['app_name'] = "Plyer Notification Example"
            if platform == "win":
                kwargs['app_icon'] = join(dirname(realpath(__file__)),
                                          'plyer-icon.ico')
                kwargs['timeout'] = 4
            else:
                kwargs['app_icon'] = join(dirname(realpath(__file__)),
                                          'plyer-icon.png')
        action = "speak"
        name = "speak"
        icon = 17301539
        callback = self.noti_callback
        buttons = []
        buttons.append([action,
                        name,
                        icon,
                        callback])
        kwargs = {'title': title,
                  'message': message,
                  'buttons': buttons}

        notification.notify(**kwargs)

    def noti_callback(self):
        osc.sendMsg('/some_api', ['callback'], port=serviceport)

    def stop_service(self):
        if self.service:
            self.service.stop()
        self.service = None

    def api_callback(self, message, *args):
        self.do_notify()
        self.serv_msg += ':::'
        self.serv_msg += '\n{}'.format(message[2])

if __name__ == '__main__':
    ServiceApp().run()
