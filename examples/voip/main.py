from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from plyer import Voip
import threading

class VOIPClientApp(App):
    # Initialize a client
    client = Voip(debug=True)  # Debug arguement is not required, but defaults to false.

    # Configure connection from client to VOIP server.
    # Alternatively, you can pass these as **kwargs to the client.start_call() method.
    client.dst_address = "192.168.1.12"  # Set to your server's IP address. Use root domain if using SSL [Required]
    client.dst_port = 8080  # Set to your server's assigned port [Required]
    client.timeout = 3  # Sets wait time to connect to server (5 seconds is default) [Optional]
    client.ssl = False  # Determines if SSL/TLS will be used (False by default) [Optional]
    client.tls_version = "TLSv1.3"  # Defaults to auto selection if empty. TLSv1.3 and TLSv1.2 are preferred options. [Optional]
    client.client_id = "user@kivy.org"  # Supports identifying/authorizing connection [Optional]
    
    def build(self):
        # Create a call and end call button to alternate between to allow client control over VOIP call
        self.layout = BoxLayout(orientation='vertical')
        self.call_button = Button(text="Call")
        self.end_call_button = Button(text="End Call", disabled=True)
        self.call_button.bind(on_press=self.start_call)
        self.end_call_button.bind(on_press=self.end_call)
        self.layout.add_widget(self.call_button)
        self.layout.add_widget(self.end_call_button)
        return self.layout
    
    def auto_end_call(self):  # Automate ending call, including if connection closes externally
        if self.client.connected and self.client.hasPermission:
            # If client is connected and has permission, call is active
            while self.client.active_call:  # Loop that runs until call ends
                pass
        if not self.end_call_button.disabled:
            instance = VOIPClientApp()
            self.end_call(instance)

    def start_call(self, instance):
	    # Disable call button after call button is pressed
        self.call_button.disabled = True
        self.end_call_button.disabled = False
        self.client.start_call()  # Initiate the VOIP call
        self.track_call_thread = threading.Thread(target=self.auto_end_call, daemon=True)
        self.track_call_thread.start()

    def end_call(self, instance):
        # Disable end call button after end call button is pressed
        self.end_call_button.disabled = True
        self.call_button.disabled = False
        self.client.end_call()  # End the VOIP call
        
if __name__ == "__main__":
    VOIPClientApp().run()
