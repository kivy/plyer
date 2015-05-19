"""Hardware example.

Shows in app current sensors, DPI and connection.
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout

from utils import instance

Builder.load_string('''
<UtilsInterface>:
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    Label:
        size_hint_y: None
        height: sp(20)
        text: 'Internet Connection: ' + str(root.hardware.is_connection())
    Label:
        size_hint_y: None
        height: sp(20)
        text: 'Display Metrics: ' + str(root.hardware.display_metrics())

    Button:
        id: button_keyboard
        height: sp(40)
        size_hint_y: None
        text: 'Show Keyboard'
        on_release: root.toggle_keyboard()

''')


class UtilsInterface(BoxLayout):
    """Main Layout."""

    hardware = instance()
    keyboard_state = 'hidden'

    def toggle_keyboard(self):
        button_keyboard = self.ids['button_keyboard']
        if self.keyboard_state == 'hidden':
            self.keyboard_state = 'show'
            self.hardware.show_keyboard()
            button_keyboard.text = 'Hide Keyboard'
        else:
            self.keyboard_state = 'hidden'
            self.hardware.hide_keyboard()
            button_keyboard.text = 'Show Keyboard'

    def add_sensors(self):

        def create_popup(title, content):
            return Popup(
                title=title,
                content=Label(text=content),
                size_hint=(None, None),
                size=(500, 700),
                auto_dismiss=True
            )

        sensors = self.hardware.get_hardware_sensors()

        stack = StackLayout()
        for sensor in sensors:
            title = sensor['name']
            content = '\n'.join(
                [key.title() + ' : ' + str(sensor[key]) for key in sensor]
            )

            button = Button(
                text=title,
                size_hint=(None, 0.15),
                width=450,
            )
            popup = create_popup(title, content)
            button.bind(on_release=popup.open)
            stack.add_widget(button)
        self.add_widget(stack)


class UtilsApp(App):
    """Main App."""

    def build(self):
        """Return root layout."""
        interface = UtilsInterface()
        interface.add_sensors()
        return interface


if __name__ == "__main__":
    UtilsApp().run()
