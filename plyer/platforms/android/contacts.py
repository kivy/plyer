"""This module provides access for contact list."""

from plyer.facades import Contacts
from plyer.platforms.android import activity

from jnius import autoclass

JavaContacts = autoclass('android.provider.ContactsContract$Contacts')
Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
ArrayList = autoclass('java.util.ArrayList')


class AndroidContacts(Contacts):

    """Android Contacts.

    .. versionadded:: 1.2.4
    """

    def refresh(self):
        """Refresh local contact list."""
        cr = activity.getContentResolver()
        contact_cr = cr.query(JavaContacts.CONTENT_URI, None, None, None, None)

        contacts = []
        while contact_cr.moveToNext():
            contact = {}

            contact_id = contact_cr.getColumnIndex(JavaContacts._ID)
            contact['contact_id'] = contact_cr.getString(contact_id)

            display_name = contact_cr.getColumnIndex('display_name')
            display_name = contact_cr.getString(display_name)
            contact['display_name'] = display_name.decode('ascii', 'ignore')

            has_phone_number = contact_cr.getColumnIndex('has_phone_number')
            has_phone_number = int(contact_cr.getString(has_phone_number))
            contact['has_phone_number'] = has_phone_number

            phone_numbers = []
            if contact['has_phone_number'] > 0:
                l = ArrayList()
                l.add(contact['contact_id'])
                query = "contact_id=?"
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
    """Return android contacts."""
    return AndroidContacts()
