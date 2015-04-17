"""Contacts module.

Implements Manager for easier management of contacts and
small instances for store information about photos, emails and addresses.
"""


class ContactManager(object):
    """Manager for receiving specific objects.

    .. versionadded:: 1.2.4

    Class for easier management contacts and groups.
    """
    _data = []

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        return self._data.__iter__()

    def __init__(self, data=None):
        """Initial Method.

        :param data: list of objects. If not given, objects will be retrieved
        from database of device.
        """
        super(ContactManager, self).__init__()
        if data is None:
            self.refresh()

    @classmethod
    def from_data(cls, initial_data):
        """Return manager from given data.

        :param initial_data: list of contacts or groups. Because of given data
        manager do not refresh itself and will handle only on given data.
        """
        self = cls(initial_data)
        return self

    @classmethod
    def filter(cls, **params):
        """Return objects filtered in params.

        :param params: dictionary where `key` is a column from object and
        value of key is compared to value of column from this object.
        Example
        -------
            >>> from plyer import contacts
            >>> kivy_contacts = contacts.filter(display_name='kivy')
            >>> print kivy_contacts
            >>> [{
                'id': 1,
                'display_name': 'kivy',
                'phones': ['123-123-123']
            }]
        """
        result = []

        # filtering objects
        for obj in cls._data:

            # filtering by params
            for column, value in params.items():
                if column in obj and obj[column] == value:
                    result.append(obj)
        return cls(result)

    def refresh(self):
        """Refresh data from db."""
        raise NotImplementedError

    @classmethod
    def all(cls):
        """Query and return all objects."""
        return cls()

    def exist(self):
        """Returns True if have any object."""
        return bool(self._data)

    def first(self):
        """Return first object from list of objects."""
        return self._data[0] if len(self._data) else None


class Contact(object):
    """Contact.

    Keeps personal info about contact like name or surname.
    Also provides access to phones, addresses and emails from that instance.

    One instance is one contact.
    Behaves like dictionary and serializes like dictionary.

    Currently available fields:

        'display_name'
        'id',
        'phones'

    Example
    ------
        >>> from plyer import contacts
        >>> contact = contacts.first()
        >>> print contact.__class__
        'Contact'
        >>> print contact.fields()
        [
            'addresses',
            'display_name',
            'emails',
            'groups',
            'id',
            'phones',
            'photos',
        ]
        >>> print contact['display_name']
        'Kivy Team'
        >>> print contact['phones']
        ['123-123-123']
    """

    _data = {}
    """Personal info about contact."""

    groups = []
    """List of groups that contact belongs to."""

    phones = []
    """List of phones that contact has."""

    addresses = []
    """List of addresses that contact has."""

    emails = []
    """List of emails that contact has."""

    photos = []
    """List of photos that contact is sticked to."""


class Group(object):
    pass


class Phone(object):
    pass


class Address(object):
    pass


class Email(object):
    pass


class Photo(object):
    pass
