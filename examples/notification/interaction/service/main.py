from time import sleep
from kivy.lib import osc
from plyer import notification
from jnius import autoclass
from android.broadcast import BroadcastReceiver

PythonActivity = autoclass('org.renpy.android.PythonActivity')
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')
NotificationBuilder = autoclass('android.app.Notification$Builder')
PythonService = autoclass('org.renpy.android.PythonService')

serviceport = 3001
activityport = 3002


class Service:
    def __init__():
        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=serviceport)
        osc.sendMsg('/some_api', ['Init'], port=activityport)
        try:
            osc.bind(oscid, self.service_callback, '/some_api')

            while True:
                osc.readQueue(oscid)
                sleep(.3)
        except:
            osc.sendMsg('/some_api', ['error'], port=activityport)

        self.br = BroadcastReceiver(self.on_broadcast,
                                    actions=['provider_changed'])
        self.br.start()

    def service_callback(message, *args):
        osc.sendMsg('/some_api', [str(message[2])], port=activityport)

    def on_broadcast(self, context, intent):
        try:
            action = intent.getAction()
            _ns = PendingIntent()
            _ns.cancel(0)
            service = PythonService.mService
            intent = Intent(service.getApplicationContext(),
                            PythonActivity)
            intent.addFlags(
                Intent.FLAG_ACTIVITY_NEW_TASK | \
                Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
            service.getApplicationContext().startActivity(intent)

        except Exception as e:
            raise Exception('Exception: ', str(e))

if __name__ == '__main__':
    service = Service()
