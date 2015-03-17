from plyer.facades import Contacts
from plyer.platforms.android import activity

from jnius import autoclass
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Contacts = autoclass('android.provider.ContactsContract$Contacts')
Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
ArrayList = autoclass('java.util.ArrayList')
String = autoclass('java/lang/String')


class AndroidContacts(Contacts):
    '''Android Contacts

    .. versionadded:: 1.2.4

    '''

    def __init__(self):
        self.refresh()

    def refresh(self):
        """Refreshes local contact list"""
        cr = activity.getContentResolver()
        contact_cr = cr.query(Contacts.CONTENT_URI, None, None, None, None)
        if contact_cr.getCount < 1:
            return

        contacts = []
        while contact_cr.moveToNext():
            contact = {}

            contact_id = contact_cr.getColumnIndex(Contacts._ID)
            contact['contact_id'] = contact_cr.getString(contact_id)

            display_name = contact_cr.getColumnIndex('display_name')
            display_name = contact_cr.getString(display_name)
            contact['display_name'] = display_name.decode('ascii', 'ignore')

            has_phone_number = contact_cr.getColumnIndex('has_phone_number')
            has_phone_number = int(contact_cr.getString(has_phone_number))
            contact['has_phone_number '] = has_phone_number

            phone_numbers = []
            if contact['has_phone_number'] > 0:
                l = ArrayList()
                l.add(contact['contact_id'])
                query = String("contact_id=?")
                phone_uri = Phone.CONTENT_URI
                phone_cr = cr.query(phone_uri, None, query, l.toArray(), None)

                while phone_cr.moveToNext():
                    phone_number = phone_cr.getColumnIndex(Phone.NUMBER)
                    phone_number = phone_cr.getString(phone_number)
                    phone_numbers.append(phone_number)
                phone_cr.close()

            contact['phone_numbers'] = phone_numbers
            contacts.append(contact)

        contact_cr.close()
        self._contacts = contacts


def instance():
    return AndroidContacts()
