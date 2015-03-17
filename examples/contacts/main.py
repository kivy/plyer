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
        from plyer.platforms.android.contacts import instance as contacts
        print contacts.get()
        # print 'python', args, kwargs
        # print 'python', Contacts
        # print 'python', ContactsContract
        # print 'python', Contacts.CONTENT_URI
        # print 'python Content URI', RawContacts.CONTENT_URI
        # # print 'python', 'displayname', Contacts.DISPLAY_NAME_PRIMARY
        # print 'python phoneuri', Phone.CONTENT_URI
        # contentResolver = activity.getContentResolver()
        # print 'python', contentResolver
        # cursor = contentResolver.query(Contacts.CONTENT_URI, None, None, None, None)
        # print 'python', 'count', cursor.getCount()
        # if cursor.getCount() == 0:
        #     return
        # print 'python', cursor
        # i = 0
        # while cursor.moveToNext():
        #     i +=1
        #     contact_id = cursor.getString(cursor.getColumnIndex(Contacts._ID))
        #     name = cursor.getString(cursor.getColumnIndex(String('display_name'))).decode('ascii', 'ignore')
        #     name = unicode(name)
        #     has_phone_number = cursor.getString(cursor.getColumnIndex('has_phone_number'))
        #     print 'python', 'details', i, name, contact_id, has_phone_number
        #     if int(has_phone_number) > 0:
        #         l = ArrayList()
        #         print 'python1'
        #         l.add(contact_id)
        #         print 'python2', Phone.CONTACT_ID, Phone.NUMBER
        #         phone_cursor = contentResolver.query(Phone.CONTENT_URI, None, String("contact_id=?"), l.toArray(), None)
        #         print 'python3', phone_cursor.getCount()
        #         while phone_cursor.moveToNext():
        #             print 'python', phone_cursor.getString(phone_cursor.getColumnIndex(Phone.NUMBER)), Phone.NUMBER
        #         phone_cursor.close()
        #
        # print 'python its end of contacts'
        #
        # String _ID = ContactsContract.Contacts._ID
        # DISPLAY_NAME = ContactsContract.Contacts.DISPLAY_NAME
        # HAS_PHONE_NUMBER = ContactsContract.Contacts.HAS_PHONE_NUMBER
        #
        # PhoneCONTENT_URI = ContactsContract.CommonDataKinds.Phone.CONTENT_URI
        # Phone_CONTACT_ID = ContactsContract.CommonDataKinds.Phone.CONTACT_ID
        # NUMBER = ContactsContract.CommonDataKinds.Phone.NUMBER
        #
        # EmailCONTENT_URI =  ContactsContract.CommonDataKinds.Email.CONTENT_URI
        # EmailCONTACT_ID = ContactsContract.CommonDataKinds.Email.CONTACT_ID
        # DATA = ContactsContract.CommonDataKinds.Email.DATA
        #
        # contentResolver = activity.getContentResolver()
        # cursor = contentResolver.query(CONTENT_URI, None,None, None, None)
        #

class ContactsApp(App):
    def build(self):
        return ContactsInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    ContactsApp().run()

