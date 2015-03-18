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

    def query(self, url, columns=None, where=None,
              where_args=None, order_by=None):
        """Gives cursor over the result set

        Android query behaves a little like SQL queries.
        With params you can read query as:
            select `columns`
            from `url`
            where `where` % `where_args`
            order by `order_by`

        :param url: address from retrieve results
        :param columns: selected columns to return. If none then return all
        :param where: args to filter results.
        :param where_args: list of strings replaced with `?` in where
        :param order_by: order of result
        :return: cursor with the results
        """

        # need to create here method .convertToJavaArray
        if columns:
            j_columns = ArrayList()
            [j_columns.add(column) for column in columns]
            columns = j_columns.toArray()

        if where_args:
            j_args = ArrayList()
            [j_args.add(param) for param in where_args]
            where_args = j_args.toArray()

        cr = activity.getContentResolver()
        return cr.query(url, columns, where, where_args, order_by)

    def refresh(self):
        """Refresh local contact list."""
        contact_cr = self.query(JavaContacts.CONTENT_URI)

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
                where = "contact_id=?"
                where_args = [contact['contact_id']]
                phone_uri = Phone.CONTENT_URI
                phone_cr = self.query(phone_uri, where=where,
                                      where_args=where_args)

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
