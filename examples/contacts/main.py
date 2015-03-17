from kivy.app import App
from jnius import autoclass
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from plyer.platforms.android import activity

PythonActivity = autoclass('org.renpy.android.PythonActivity')
ContactsContract = autoclass('android.provider.ContactsContract')
Contacts = autoclass('android.provider.ContactsContract$Contacts')
RawContacts = autoclass('android.provider.ContactsContract$RawContacts')

Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')

ArrayList = autoclass('java.util.ArrayList')
Object = autoclass('java.lang.Object')
String = autoclass('java/lang/String')

Builder.load_string('''
<ContactsInterface>:
    id: contacts
    orientation: 'vertical'
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Contact List'
    Button:
        text: 'get contacts'
        on_release: contacts.vpress()
''')


class ContactsInterface(BoxLayout):

    def vpress(self, *args, **kwargs):
        from plyer import contacts
        print 'python', contacts.get()
        
class ContactsApp(App):
    def build(self):
        return ContactsInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    ContactsApp().run()

