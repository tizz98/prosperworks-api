from . import api
from . import utils


class Model(utils.QuickRepr):
    _endpoint = None
    _id_field = 'id'
    _lazy_props = tuple()

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
            elif isinstance(current_value, object) and callable(current_value):
                if hasattr(current_value, 'populate'):
                    new_value = current_value()
                    setattr(self, key, new_value.populate(value))
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

    def serialize(self, *fields):
        fields = fields or self.get_fields()
        return {
            key: getattr(self, key)
            if not hasattr(getattr(self, key), 'serialize')
            else getattr(self, key).serialize()
            for key in fields
            if key not in self._lazy_props
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

    def update(self, *fields):
        data = self.serialize(*fields)
        response = api.requests.put(self.id_url, json=data)
        self.populate(data=response)


class ListableModel(Model):
    """
    A Model that is listable via .list
    """

    @classmethod
    def list(cls):
        results = api.requests.get(cls._endpoint)
        return cls.populate_list(list_data=results)


class SearchableModel(ListableModel):
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

    @classmethod
    def list(cls):
        return cls.search()


class ObjectList(utils.QuickRepr, utils.AbstractMixin):
    def __init__(self, model, objects=None):
        self.model = model
        self.objects = objects or list()

    def populate(self, objects):
        self.objects = [
            self.model.from_simple_dict(obj) for obj in objects
        ]
        return self

    def serialize(self):
        return [obj.serialize() for obj in self.objects]

    def __iter__(self):
        return self.objects.__iter__()

    def __call__(self, *args, **kwargs):
        return super(ObjectList, self).__call__(self.model, *args, **kwargs)


class SimpleList(utils.QuickRepr, utils.AbstractMixin):
    def __init__(self, objects=None):
        self.objects = objects or list()

    def populate(self, objects):
        self.objects = objects
        return self

    def serialize(self):
        return self.objects

    def __iter__(self):
        return self.objects.__iter__()


class SimpleObject(utils.Data, utils.AbstractMixin):
    _raw = {}

    def __init__(self, **kwargs):
        super(SimpleObject, self).__init__(**kwargs)
        self._raw = kwargs

    def populate(self, data=None):
        self._raw = data or {}
        return super(SimpleObject, self).populate(data)

    def serialize(self):
        return self._raw


class Account(Model):
    _endpoint = "account"

    id = None
    name = None

    @classmethod
    def get_account(cls):
        return cls().populate()


class Address(Model, utils.AbstractMixin):
    street = None
    city = None
    state = None
    postal_code = None
    country = None


class PhoneNumber(Model):
    number = None
    category = None


class Email(Model):
    email = None
    category = None


class Social(Model):
    url = None
    category = None


class Website(Model):
    url = None
    category = None


class CustomField(ListableModel):
    _endpoint = "custom_field_definitions"
    _id_field = 'custom_field_definition_id'

    custom_field_definition_id = None
    value = None
    name = None
    data_type = None


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
        'phone_numbers',
        'socials',
        'tags',
        'websites',
        'date_created',
        'date_modified',
        'custom_fields',
    )
    _lazy_props = (
        'assignee',
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

    @utils.lazy_property
    def assignee(self):
        return User(self.assignee_id)

    @utils.lazy_property
    def contact_type(self):
        if self.contact_type_id:
            contact_types = api.cache.get_or_set(
                "contact_types",
                lambda: ContactType.list()
            )
            results = filter(
                lambda x: x.id == self.contact_type_id,
                contact_types
            )
            if len(results) == 1:
                return results[0]
        return None


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
        'phone_numbers',
        'socials',
        'status',
        'tags',
        'title',
        'websites',
        'date_created',
        'date_modified',
        'custom_fields',
    )
    _lazy_props = (
        'assignee',
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

    @utils.lazy_property
    def assignee(self):
        return User(self.assignee_id)


class Opportunity(CRUDModel, SearchableModel):
    _endpoint = "opportunities"
    _search_fields = (
        'page_number',
        'page_size',
        'sort_by',
        'sort_direction',
        'tags',
        'assignee_ids',
        'customer_source_ids',
        'loss_reason_ids',
        'pipeline_ids',
        'pipeline_stage_ids',
        'priorities',
        'minimum_close_date',
        'maximum_close_date',
        'minimum_monetary_value',
        'maximum_monetary_value',
        'minimum_stage_change_date',
        'maximum_stage_change_date',
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
        'primary_contact_id',
        'assignee_id',
        'company_id',
        'close_date',
        'customer_source_id',
        'details',
        'loss_reason_id',
        'monetary_value',
        'pipeline_id',
        'priority',
        'pipeline_stage_id',
        'status',
        'tags',
        'win_probability',
        'custom_fields',
    )
    _lazy_props = (
        'company',
        'assignee',
        'primary_contact',
    )

    id = None
    name = None
    assignee_id = None
    close_date = None
    company_id = None
    company_name = None
    customer_source_id = None
    details = None
    loss_reason_id = None
    monetary_value = None
    pipeline_id = None
    primary_contact_id = None
    priority = None
    pipeline_stage_id = None
    status = None
    tags = SimpleList()
    win_probability = None
    date_created = None
    date_modified = None
    custom_fields = ObjectList(CustomField)

    @utils.lazy_property
    def company(self):
        return Company(self.company_id)

    @utils.lazy_property
    def assignee(self):
        return User(self.assignee_id)

    @utils.lazy_property
    def primary_contact(self):
        return Person(self.primary_contact_id)


class Person(CRUDModel, SearchableModel):
    _endpoint = "people"
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
        'company_id',
        'contact_type_id',
        'details',
        'emails',
        'phone_numbers',
        'socials',
        'tags',
        'title',
        'websites',
        'date_created',
        'date_modified',
        'custom_fields',
    )
    _lazy_props = (
        'company',
        'assignee',
        'contact_type',
    )

    id = None
    name = None
    address = Address()
    assignee_id = None
    company_id = None
    company_name = None
    contact_type_id = None
    details = None
    emails = ObjectList(Email)
    phone_numbers = ObjectList(PhoneNumber)
    socials = ObjectList(Social)
    tags = SimpleList()
    title = None
    websites = ObjectList(Website)
    date_created = None
    date_modified = None
    custom_fields = ObjectList(CustomField)

    @utils.lazy_property
    def company(self):
        return Company(self.company_id)

    @utils.lazy_property
    def assignee(self):
        return User(self.assignee_id)

    @utils.lazy_property
    def contact_type(self):
        if self.contact_type_id:
            contact_types = api.cache.get_or_set(
                "contact_types",
                lambda: ContactType.list()
            )
            results = filter(
                lambda x: x.id == self.contact_type_id,
                contact_types
            )
            if len(results) == 1:
                return results[0]
        return None

    @classmethod
    def fetch_by_email(cls, email):
        """
        Note: If a Person with the email is not found, this endpoint will
        return a 404 and thus this api wrapper will raise
        prosperworks.exceptions.ProsperWorksNotFoundRequest
        """
        data = api.requests.post(cls._endpoint + "/fetch_by_email", json={
            'email': email
        })
        person = cls()
        return person.populate(data=data)


class User(SearchableModel):
    _endpoint = "users"
    _search_fields = (
        'page_number',
        'page_size',
        'sort_by',
        'sort_direction',
    )

    id = None
    name = None
    email = None


class Task(CRUDModel, SearchableModel):
    _endpoint = "tasks"
    _lazy_props = (
        'assignee',
    )
    _search_fields = (
        'page_number',
        'page_size',
        'sort_by',
        'sort_direction',
        'name',
        'assignee_ids',
        'statuses',
        'priorities',
        'tags',
        'minimum_due_date',
        'maximum_due_date',
        'minimum_reminder_date',
        'maximum_reminder_date',
        'minimum_completed_date',
        'maximum_completed_date',
        'minimum_created_date',
        'maximum_created_date',
        'minimum_modified_date',
        'maximum_modified_date',
    )
    _create_fields = (
        'name',
        'related_resource',
        'assignee_id',
        'due_date',
        'reminder_date',
        'priority',
        'status',
        'details',
        'tags',
        'custom_fields',
    )

    id = None
    name = None
    related_resource = SimpleObject
    assignee_id = None
    due_date = None
    reminder_date = None
    completed_date = None
    priority = None
    status = None
    details = None
    tags = SimpleList
    custom_fields = ObjectList(CustomField)
    date_created = None
    date_modified = None

    @utils.lazy_property
    def assignee(self):
        return User(self.assignee_id)


class Project(CRUDModel, SearchableModel):
    _endpoint = "projects"
    _search_fields = (
        'page_number',
        'page_size',
        'sort_by',
        'sort_direction',
        'name',
        'assignee_ids',
        'statuses',
        'tags',
        'minimum_created_date',
        'maximum_created_date',
        'minimum_modified_date',
        'maximum_modified_date',
    )
    _create_fields = (
        'name',
        'related_resource',
        'assignee_id',
        'status',
        'details',
        'tags',
        'custom_fields',
    )
    _lazy_props = (
        'assignee',
    )

    id = None
    name = None
    related_resource = SimpleObject
    assignee_id = None
    status = None
    details = None
    tags = SimpleList
    custom_fields = ObjectList(CustomField)
    date_created = None
    date_modified = None

    @utils.lazy_property
    def assignee(self):
        return User(self.assignee_id)


class CustomerSource(ListableModel):
    _endpoint = "customer_sources"

    id = None
    name = None


class LossReason(ListableModel):
    _endpoint = "loss_reasons"

    id = None
    name = None


class PipelineStage(ListableModel):
    _endpoint = "pipeline_stages"
    _lazy_props = (
        'pipeline',
    )

    id = None
    name = None
    pipeline_id = None
    win_probability = None

    @utils.lazy_property
    def pipeline(self):
        if self.pipeline_id:
            pipelines = api.cache.get_or_set(
                "pipelines",
                lambda: Pipeline.list()
            )
            results = filter(lambda x: x.id == self.pipeline_id, pipelines)
            if len(results) == 1:
                return results[0]
        return None


class Pipeline(ListableModel):
    _endpoint = "pipelines"

    id = None
    name = None
    stages = ObjectList(PipelineStage)


class ContactType(ListableModel):
    _endpoint = "contact_types"

    id = None
    name = None
