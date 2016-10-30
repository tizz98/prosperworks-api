class Model(object):
    _endpoint = NotImplemented
    _id_field = 'id'

    def __init__(self, id=None):
        setattr(self, self._id_field, id)

    def populate(self, api, data=None):
        data = data or api.requests.get(
            self._endpoint + "/" + (getattr(self, self._id_field) or '')
        )
        for key, value in data.items():
            if getattr(self, key) is None:
                setattr(self, key, value)
            elif isinstance(getattr(self, key), object):
                other_cls = getattr(self, key)
                setattr(self, key, other_cls.populate(api, value))
        return self

    @classmethod
    def from_simple_dict(cls, simple_dict):
        obj = cls()
        for key, value in simple_dict.items():
            setattr(obj, key, value)
        return obj

    def __repr__(self):
        return "<%s: %s>" % (
            self.__class__.__name__,
            ', '.join(
                "%s=%s" % (key, str(getattr(self, key)))
                for key in self.__dict__
                if not key.startswith('_')
            )
        )


class ObjectList(object):
    def __init__(self, model, objects=None):
        self.model = model
        self.objects = objects or list()

    def populate(self, api, objects):
        self.objects = [
            self.model.from_simple_dict(obj) for obj in objects
        ]


class SimpleList(object):
    def __init__(self, objects=None):
        self.objects = objects or list()

    def populate(self, api, objects):
        self.objects = objects


class Account(Model):
    _endpoint = "account"

    id = None
    name = None


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
