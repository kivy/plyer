from time import sleep
from kivy.lib import osc
from android.broadcast import BroadcastReceiver

serviceport = 3001
activityport = 3002

def service_callback(message, *args):
    osc.sendMsg('/some_api', [str(message[2])], port=activityport)

class Service:
    def __init__(self):
        sleep(1)
        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=serviceport)
        try:
            osc.sendMsg('/some_api', ['Init'], port=activityport)
            osc.bind(oscid, service_callback, '/some_api')

            while True:
                osc.readQueue(oscid)
                sleep(.3)
        except:
            osc.sendMsg('/some_api', ['error'], port=activityport)

        self.br = BroadcastReceiver(self.on_broadcast,
                                    actions=['provider_changed'])
        self.br.start()

    def service_callback(self, message, *args):
        osc.sendMsg('/some_api', [str(message[2])], port=activityport)

    def on_broadcast(self, context, intent):
        pass
        '''
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
        '''


if __name__ == '__main__':
    service = Service()
