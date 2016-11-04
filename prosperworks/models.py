from . import api
from . import exceptions


class Model(object):
    _endpoint = NotImplemented
    _id_field = 'id'

    def __init__(self, id=None):
        setattr(self, self._id_field, id)

    def populate(self, data=None):
        data = data or api.requests.get(
            self._endpoint + "/" + (getattr(self, self._id_field) or '')
        )
        for key, value in data.items():
            if getattr(self, key) is None:
                setattr(self, key, value)
            elif isinstance(getattr(self, key), object):
                other_cls = getattr(self, key)
                if hasattr(other_cls, 'populate'):
                    setattr(self, key, other_cls.populate(value))
        return self

    @classmethod
    def populate_list(cls, list_data=None):
        objects = []
        list_data = list_data or api.requests.get(cls._endpoint)

        for data in list_data:
            obj = cls()
            obj.populate(data=data)
            objects.append(obj)

        return objects

    @classmethod
    def from_simple_dict(cls, simple_dict):
        obj = cls()
        for key, value in simple_dict.items():
            setattr(obj, key, value)
        return obj

    def __unicode__(self):
        return repr(self)

    def __repr__(self):
        return u"<%s: %s>" % (
            self.__class__.__name__,
            u', '.join(
                u"%s=%s" % (key, str(getattr(self, key)))
                for key in self.__dict__
                if not key.startswith('_')
            )
        )


class ObjectList(object):
    def __init__(self, model, objects=None):
        self.model = model
        self.objects = objects or list()

    def populate(self, objects):
        self.objects = [
            self.model.from_simple_dict(obj) for obj in objects
        ]


class SimpleList(object):
    def __init__(self, objects=None):
        self.objects = objects or list()

    def populate(self, objects):
        self.objects = objects


class Account(Model):
    _endpoint = "account"

    id = None
    name = None

    @classmethod
    def get_account(cls):
        return cls().populate()


class Address(Model):
    street = None
    city = None
    state = None
    postal_code = None
    country = None


class PhoneNumber(Model):
    number = None
    category = None


class Social(Model):
    url = None
    category = None


class Website(Model):
    url = None
    category = None


class CustomField(Model):
    _id_field = 'custom_field_definition_id'

    custom_field_definition_id = None
    value = None


class Company(Model):
    _endpoint = "companies"
    _search_fields = (
        'page_number',
        'page_size',
        'sort_by',
        'sort_direction',
        'tags',
        'age',
        'assignee_ids',
        'city',
        'state',
        'postal_code',
        'country',
        'minimum_interaction_count',
        'maximum_interaction_count',
        'minimum_interaction_date',
        'maximum_interaction_date',
        'minimum_created_date',
        'maximum_created_date',
        'minimum_modified_date',
        'maximum_modified_date',
    )

    id = None
    name = None
    address = Address()
    assignee_id = None
    contact_type_id = None
    details = None
    email_domain = None
    phone_numbers = ObjectList(PhoneNumber)
    socials = ObjectList(Social)
    tags = SimpleList()
    websites = ObjectList(Website)
    date_created = None
    date_modified = None
    custom_fields = ObjectList(CustomField)

    @classmethod
    def search(cls, **query_fields):
        for field in query_fields.keys():
            if field not in cls._search_fields:
                raise exceptions.ProsperWorksApplicationException(
                    "%s is not a valid search field." % field
                )

        results = api.requests.post(cls._endpoint + "/search", query_fields)
        return cls.populate_list(list_data=results)
