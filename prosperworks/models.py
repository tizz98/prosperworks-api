from . import api
from . import utils


class Model(utils.QuickRepr):
    _endpoint = None
    _id_field = 'id'

    def __init__(self, id=None):
        setattr(self, self._id_field, id)

        if id is not None:
            self.populate()

    @property
    def id_url(self):
        return "{}/{}".format(
            self._endpoint,
            getattr(self, self._id_field) or ''
        )

    def populate(self, data=None):
        if self._endpoint is None and data is None:
            return data
        data = data or api.requests.get(self.id_url)
        for key, value in data.items():
            current_value = getattr(self, key, None)
            if current_value is None:
                setattr(self, key, value)
            elif isinstance(current_value, object):
                if hasattr(current_value, 'populate'):
                    setattr(self, key, current_value.populate(value))
        return self

    @classmethod
    def populate_list(cls, list_data=None):
        objects = []

        if list_data is None:
            list_data = api.requests.get(cls._endpoint)

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

    def serialize(self):
        return {
            key: getattr(self, key)
            if not hasattr(getattr(self, key), 'serialize')
            else getattr(self, key).serialize()
            for key in self.get_fields()
        }


class CRUDModel(Model):
    """
    A Model that can be created (.create), retrieved (__init__),
    updated (.update) & deleted (.delete)
    """
    _create_fields = tuple()

    def delete(self):
        response = api.requests.delete(self.id_url)
        return utils.Data(**response)

    @classmethod
    def create(cls, **create_fields):
        utils.validate_fields(create_fields, cls._create_fields)
        response = api.requests.post(cls._endpoint, json=create_fields)
        return cls().populate(data=response)

    def update(self):
        data = self.serialize()
        response = api.requests.put(self.id_url, json=data)
        self.populate(data=response)


class SearchableModel(Model):
    """
    A Model that is searchable via .search
    """
    _search_fields = tuple()
    _search_path = 'search'

    @classmethod
    def search_endpoint(cls):
        return "{}/{}".format(cls._endpoint, cls._search_path)

    @classmethod
    def search(cls, **query_fields):
        utils.validate_fields(query_fields, cls._search_fields, 'search')
        results = api.requests.post(cls.search_endpoint(), query_fields)
        return cls.populate_list(list_data=results)


class ObjectList(utils.QuickRepr):
    def __init__(self, model, objects=None):
        self.model = model
        self.objects = objects or list()

    def populate(self, objects):
        self.objects = [
            self.model.from_simple_dict(obj) for obj in objects
        ]

    def serialize(self):
        return [obj.serialize() for obj in self.objects]


class SimpleList(utils.QuickRepr):
    def __init__(self, objects=None):
        self.objects = objects or list()

    def populate(self, objects):
        self.objects = objects

    def serialize(self):
        return self.objects


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


class Company(CRUDModel, SearchableModel):
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
    _create_fields = (
        'name',
        'address',
        'assignee_id',
        'contact_type_id',
        'details',
        'email_domain',
        'phone_numbers[]',
        'socials[]',
        'tags',
        'websites[]',
        'date_created',
        'date_modified',
        'custom_fields[]',
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


class Lead(CRUDModel, SearchableModel):
    _endpoint = "leads"
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
    _create_fields = (
        'name',
        'address',
        'assignee_id',
        'company_name',
        'customer_source_id',
        'details',
        'email',
        'monetary_value',
        'phone_numbers[]',
        'socials[]',
        'status',
        'tags',
        'title',
        'websites[]',
        'date_created',
        'date_modified',
        'custom_fields[]',
    )

    id = None
    name = None
    address = Address()
    assignee_id = None
    company_name = None
    customer_source_id = None
    details = None
    email = None
    monetary_value = None
    phone_numbers = ObjectList(PhoneNumber)
    socials = ObjectList(Social)
    status = None
    tags = SimpleList()
    title = None
    websites = ObjectList(Website)
    date_created = None
    date_modified = None
    custom_fields = ObjectList(CustomField)

    def convert(self, person=None, company=None, opportunity=None):
        details = {}

        if person:
            details['person'] = {
                'name': person.name,
                'contact_type_id': person.contact_type_id,
                'assignee_id': person.assignee_id,
            }
        if company:
            details['company'] = {
                'id': company.id,
            }
        if opportunity:
            details['opportunity'] = {
                'name': opportunity.name,
                'pipeline_id': opportunity.pipeline_id,
                'monetary_value': opportunity.monetary_value,
                'assignee_id': opportunity.assignee_id,
            }

        response = api.requests.post(
            self.id_url + "/convert",
            json={'details': details}
        )

        return utils.Data(**response)
