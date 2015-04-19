"""This module provides access for android contact list."""

from plyer.facades import Contacts
from plyer.platforms.android import activity

from jnius import autoclass

from contact_utils import AbstractContact
from contact_utils import AbstractManager
from contact_utils import AbstractPhone


JavaContacts = autoclass('android.provider.ContactsContract$Contacts')
Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
ArrayList = autoclass('java.util.ArrayList')


def query(url, columns=None, params=None, order_by=None):
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


class AndroidContact(AbstractContact):

    def reload(self):
        """Run query in android Contacts for exactly that contact.

        Required column:
            :id
        """
        id = self['id']
        if not id:
            raise AttributeError('ID cannot be None.')

        url = JavaContacts.CONTENT_URI
        params = {JavaContacts._ID: str(self['id'])}

        q = query(url, params=params)
        if not q.moveToNext():
            return False

        contact_id = q.getColumnIndex(JavaContacts._ID)
        contact_id = q.getString(contact_id)
        self['id'] = contact_id

        display_name = q.getColumnIndex('display_name')
        display_name = q.getString(display_name)
        self['display_name'] = display_name.decode('ascii', 'ignore')

        has_phone_numbers = int(q.getColumnIndex('has_phone_number'))
        q.close()

        # querying phone numbers
        phone_numbers = []
        phone_uri = Phone.CONTENT_URI

        phone_q = query(phone_uri, params={'contact_id': contact_id})
        while has_phone_numbers and phone_q.moveToNext():
            phone_number = phone_q.getColumnIndex(Phone.NUMBER)
            phone_number = phone_q.getString(phone_number)

            phone = AndroidPhone.from_params(
                number=phone_number,
                contact_id=contact_id
            )
            phone_numbers.append(phone)
        phone_q.close()

        phone_manager = AndroidPhoneNumbers.from_data(phone_numbers)
        self['phone_numbers'] = phone_manager


class AndroidPhone(AbstractPhone):
    pass


class AndroidPhoneNumbers(AbstractManager):

    def reload(self):
        pass


class AndroidContacts(Contacts):

    """Android Contacts.

    .. versionadded:: 1.2.4
    """

    def reload(self):
        """Refresh local contact list."""
        contact_q = query(JavaContacts.CONTENT_URI, columns=[JavaContacts._ID])

        contacts = []
        while contact_q.moveToNext():
            contact_id = contact_q.getColumnIndex(JavaContacts._ID)
            contact_id = contact_q.getString(contact_id)

            contact = AndroidContact.from_params(id=contact_id)
            contact.reload()
            contacts.append(contact)

        contact_q.close()
        self._data = contacts


def instance():
    """Return android contacts."""
    contacts = AndroidContacts()
    return contacts
