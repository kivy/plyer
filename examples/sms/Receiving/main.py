from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from plyer.facades import SmsReceive

Builder.load_string(
'''
<ReceiveSmsInteface>:
	orientation: 'vertical'
	Label:
		text: Receive SMS Interface
		
	BroadcastButton:
		text: "Press to start service"
		on_release: self.start()

'''
)

class ReceiveSmsInterface(BoxLayout):
	pass

class BroadcastButton(Button):
	def start(self):
		SmsReceive.receive()

class ReceiveSmsApp(App):
	def build(self):
		return ReceiveSmsInterface()

if __name__ == '__main__':
	ReceiveSmsApp().run()
