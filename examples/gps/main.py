from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.clock import mainthread
from kivy.utils import platform

kv = '''

<ProviderToggleButton@ToggleButton>:
    red: rgba('#8B0000')
    black: rgba('#ffffff')
    state: 'down'
    unavailable: True if self.text not in app.available_providers else False
    disabled: True if (self.unavailable or app.gps_running) else False
    background_color: self.red if self.unavailable else self.black

BoxLayout:
    orientation: 'vertical'
    provider_buttons: [gps_provider_button, network_provider_button, passive_provider_button]
    
    Label:
        text: "Available providers: \\n" + ((', ').join(app.available_providers) if app.available_providers else "None")
        halign: 'center'
        
    Label:
        text: app.gps_location
        
    Label:
        text: app.gps_status
        
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '48dp'
        padding: '4dp'
        
        ProviderToggleButton:
            id: gps_provider_button
            text: 'gps'
            
        ProviderToggleButton:
            id: network_provider_button
            text: 'network'
            state: 'down'
            
        ProviderToggleButton:
            id: passive_provider_button
            text: 'passive'
            state: 'down'
            
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'
        
        ToggleButton:
            id: gps_toggle_button
            text: 'Start' if self.state == 'normal' else 'Stop'
            on_state:
                app.start(1000, 0) if self.state == 'down' else \
                app.stop()
'''


class GpsTest(App):
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    available_providers = ListProperty()
    gps_running = BooleanProperty(False)

    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")
                self.gps_status = "Some permissions refused."

            self.available_providers = gps.get_available_providers()

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)

        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])

    def build(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
            self.available_providers = gps.get_available_providers()
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

        return Builder.load_string(kv)

    def start(self, minTime, minDistance):
        self.available_providers = gps.get_available_providers()
        excluded_providers = [button.text for button in self.root.provider_buttons if button.state == 'normal']
        gps.start(minTime, minDistance, excluded_providers)
        self.gps_running = True

    def stop(self):
        gps.stop()
        self.gps_running = False

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        if self.gps_running:
            self.start(1000, 0)


if __name__ == '__main__':
    GpsTest().run()
