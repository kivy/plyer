"""This module provides access for android contact list."""

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

    def query(self, url, columns=None, params=None, order_by=None):
        """Gives cursor over the result set.

        Android query behaves a little like SQL queries.
        With params you can read query as:
            select `columns`
            from `url`
            where `params`
            order by `order_by`

        :param url: str, address which query would retrieve results
        :param columns: list of str, list of columns that query will return.
            If none then return all columns.
        :param params: dict of str:str, params included in clause `where`.
        :param order_by: order of result
        :return: cursor with the results
        """

        # need to create here method .convertToJavaArray
        if columns:
            j_columns = ArrayList()
            [j_columns.add(column) for column in columns]
            columns = j_columns.toArray()

        where_params, where_args = None, None
        if params:
            where_params = '&'.join(['%s=?' % key for key in params.keys()])

            j_args = ArrayList()
            [j_args.add(val) for val in params.values()]
            where_args = j_args.toArray()

        cr = activity.getContentResolver()
        return cr.query(url, columns, where_params, where_args, order_by)

    def refresh(self):
        """Refresh local contact list."""
        contact_cr = self.query(JavaContacts.CONTENT_URI)

        contacts = []
        i = 50
        while contact_cr.moveToNext() and i > 5:
            i -= 1
            # print i, i+1, i+5
            contact = {}

            contact_id = contact_cr.getColumnIndex(JavaContacts._ID)
            contact_id = contact_cr.getString(contact_id)

            display_name = contact_cr.getColumnIndex('display_name')
            display_name = contact_cr.getString(display_name)
            display_name = display_name.decode('ascii', 'ignore')

            has_phones = int(contact_cr.getColumnIndex('has_phone_number'))

            phone_numbers = []
            if has_phones > 0:
                phone_uri = Phone.CONTENT_URI
                phone_cr = self.query(phone_uri,
                                      params={'contact_id': contact_id})

                while phone_cr.moveToNext():
                    phone_number = phone_cr.getColumnIndex(Phone.NUMBER)
                    phone_number = phone_cr.getString(phone_number)
                    phone_numbers.append(phone_number)
                phone_cr.close()

            contact['id'] = contact_id
            contact['display_name'] = display_name
            contact['phones'] = phone_numbers
            contacts.append(contact)

        contact_cr.close()
        self._data = contacts


def instance():
    """Return android contacts."""
    contacts = AndroidContacts()
    return contacts
