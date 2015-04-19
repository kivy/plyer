"""Contacts module.

Implements Manager for easier management of contacts and
small instances for store information about photos, emails and addresses.
"""
from abc import ABCMeta


class AbstractManager(object):
    """Manager for receiving specific objects.

    .. versionadded:: 1.2.4

    Class for easier management contacts and groups.
    """
    __metaclass__ = ABCMeta
    _data = []

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        return self._data.__iter__()

    def __str__(self):
        return '%s' % self._data

    def __repr__(self):
        return '%r' % self._data

    def __init__(self, initial_data=None):
        """Initial Method.

        :param data: list of objects. If not given, objects will be retrieved
        from database of device.
        """
        super(AbstractManager, self).__init__()
        if initial_data:
            if not isinstance(initial_data, list):
                raise TypeError('Wrong type of data. Use List Type.')
            self._data = initial_data

    @classmethod
    def from_data(cls, initial_data):
        """Return manager from given data.

        :param initial_data: list of contacts or groups. Because of given data
        manager do not refresh itself and will handle only on given data.
        """
        self = cls(initial_data)
        return self

    def filter(self, **params):
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
        for obj in self._data:
            # filtering by params
            for column, value in params.items():
                if column in obj and obj[column] == value:
                    result.append(obj)

        return AbstractManager.from_data(result)

    def reload(self):
        """Reload data from db."""
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

    def last(self):
        """Return last object from list."""
        return self._data[-1] if self._data else None


class AbstractDBObject(object):
    __metaclass__ = ABCMeta
    _columns = {}
    _relations = {}

    def __init__(self):
        super(AbstractDBObject, self).__init__()
        self._columns = dict(**self._columns)
        self._relations = dict(**self._relations)

    def __getitem__(self, item):
        if item in self._columns:
            return self._columns[item]
        if item in self._relations:
            return self._relations[item]
        return None

    def __setitem__(self, key, value):
        if key in self._columns:
            self._columns[key] = value
        if key in self._relations:
            self._relations[key] = value

    def __contains__(self, item):
        if item in self._columns:
            return True
        return False

    @classmethod
    def from_params(cls, **initial_data):
        """Creates objects from params.

        Fulfils columns with value from parameters.
        :param initial_data: dictionary where key is a column name
        and value is a value of that column.
        """
        self = cls()

        for key, value in initial_data.iteritems():
            if key in self._columns:
                self._columns[key] = value

        return self

    def fields(self):
        """Return list of available fields."""
        return self._columns.keys()

    def save(self):
        """Save object."""
        raise NotImplementedError

    def translate(self):
        """Return structured data for current platform."""
        raise NotImplementedError

    def reload(self):
        """Reload object from device."""
        raise NotImplementedError


class AbstractContact(AbstractDBObject):
    """Abstract Contact.

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
        >>> print contact['phone_numbers']
        ['123-123-123']
    """

    def __str__(self):
        return 'display_name:%s id:%s' % (self['display_name'], self['id'])

    __metaclass__ = ABCMeta

    _columns = {
        'id': basestring,
        'display_name': basestring
    }

    _relations = {
        # List of groups that contact belongs to.
        'groups': AbstractManager,

        # List of phones that contact has.
        'phone_numbers': AbstractManager,

        # List of addresses that contact has.
        'addresses': AbstractManager,

        # List of emails that contact has.
        'emails': AbstractManager,

        # List of photos that contact that stick to.
        'photos': AbstractManager

    }


class AbstractGroup(AbstractDBObject):
    __metaclass__ = ABCMeta
    _columns = {
        'id': int,
        'name': basestring
    }


class AbstractPhone(AbstractDBObject):
    __metaclass__ = ABCMeta
    _columns = {
        'contact_id': basestring,
        'number': basestring
    }

    def __str__(self):
        return '%s' % (self['number'])

    def __repr__(self):
        return '%r:%r' % (self['contact_id'], self['number'])


class AbstractAddress(AbstractDBObject):
    __metaclass__ = ABCMeta
    _columns = {}


class AbstractEmail(AbstractDBObject):
    __metaclass__ = ABCMeta
    _columns = {}


class AbstractPhoto(AbstractDBObject):
    __metaclass__ = ABCMeta
    _columns = {}
