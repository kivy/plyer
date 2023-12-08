from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from plyer import keystore


class KeyStoreTestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = None
        self.set_key_input = None
        self.set_value_input = None
        self.get_key_input = None
        self.get_value_label = None

    def build(self):
        self.store = keystore

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input for setting a key
        self.set_key_input = TextInput(text='Enter key to set', size_hint=(1, 0.1))
        self.set_value_input = TextInput(text='Enter value to set', size_hint=(1, 0.1))
        set_button = Button(text='Set Key', size_hint=(1, 0.1))
        set_button.bind(on_press=self.set_key)

        # Input for getting a key
        self.get_key_input = TextInput(text='Enter key to get', size_hint=(1, 0.1))
        self.get_value_label = Label(text='Value will appear here', size_hint=(1, 0.1))
        get_button = Button(text='Get Key', size_hint=(1, 0.1))
        get_button.bind(on_press=self.get_key)

        layout.add_widget(self.set_key_input)
        layout.add_widget(self.set_value_input)
        layout.add_widget(set_button)
        layout.add_widget(self.get_key_input)
        layout.add_widget(self.get_value_label)
        layout.add_widget(get_button)

        return layout

    def set_key(self, instance):
        key = self.set_key_input.text
        value = self.set_value_input.text
        self.store.set_key('servicename', key, value)
        self.set_key_input.text = ''
        self.set_value_input.text = ''

    def get_key(self, instance):
        key = self.get_key_input.text
        value = self.store.get_key('servicename', key)
        self.get_value_label.text = f'Value: {value}'
        self.get_key_input.text = ''


if __name__ == '__main__':
    KeyStoreTestApp().run()
