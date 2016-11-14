# Prosperworks Api
A python based api wrapper for [Prosperworks](https://www.prosperworks.com/developer_api). [![Build Status](https://travis-ci.org/tizz98/prosperworks-api.svg)](https://travis-ci.org/tizz98/prosperworks-api)

## Installation
From pip (recommended): `pip install prosperworks`

From source: `pip install git+git://github.com:tizz98/prosperworks-api.git@master`

# Models
## `prosperworks.models.Company`
#### Fields
- id
- name
- address (`prosperworks.models.Address`)
- assignee_id
- contact_type_id
- details
- email_domain
- phone_numbers (list of `prosperworks.models.PhoneNumber`)
- socials (list of `prosperworks.models.Social`)
- tags (list of strings)
- websites (list of `prosperworks.models.Website`)
- date_created
- date_modified
- custom_fields (list of `prosperworks.models.CustomField`)

#### Methods
- `search` (search for companies), available kwargs are:
  - page_number
  - page_size
  - sort_by
  - sort_direction
  - tags
  - age
  - assignee_ids
  - city
  - state
  - postal_code
  - country
  - minimum_interaction_count
  - maximum_interaction_count
  - minimum_interaction_date
  - maximum_interaction_date
  - minimum_created_date
  - maximum_created_date
  - minimum_modified_date
  - maximum_modified_date
- `create` (create new company), available kwargs are:
  - name
  - address
  - assignee_id
  - contact_type_id
  - details
  - email_domain
  - phone_numbers[]
  - socials[]
  - tags
  - websites[]
  - date_created
  - date_modified
  - custom_fields[]
- `update` (update current company), _will use currently set values to update_
- `delete` (delete current company)


#### Examples:
```python
from prosperworks import api
from prosperworks.models import Company

api.configure('key', 'your.name@example.com')
for company in Company.search():
    print company.name

new_co = Company.create(name='New Co.')
print new_co.id

new_co.name = 'New Co. (updated)'
new_co.update()

new_co.delete()
```

## `prosperworks.models.Lead`
#### Fields
- id
- name
- address (`prosperworks.models.Address`)
- assignee_id
- company_name
- customer_source_id
- details
- email
- monetary_value
- phone_numbers (list of `prosperworks.models.PhoneNumber`)
- socials (list of `prosperworks.models.Social`)
- status
- tags (list of strings)
- websites (list of `prosperworks.models.Website`)
- date_created
- date_modified
- custom_fields (list of `prosperworks.models.CustomField`)

#### Methods
- `search` (search for companies), available kwargs are:
  - page_number
  - page_size
  - sort_by
  - sort_direction
  - tags
  - age
  - assignee_ids
  - city
  - state
  - postal_code
  - country
  - minimum_interaction_count
  - maximum_interaction_count
  - minimum_interaction_date
  - maximum_interaction_date
  - minimum_created_date
  - maximum_created_date
  - minimum_modified_date
  - maximum_modified_date
- `create` (create new company), available kwargs are:
  - name
  - address
  - assignee_id
  - company_name
  - customer_source_id
  - details
  - email
  - monetary_value
  - phone_numbers[]
  - socials[]
  - status
  - tags
  - title
  - websites[]
  - date_created
  - date_modified
  - custom_fields[]
- `update` (update current company), _will use currently set values to update_
- `delete` (delete current company)
- `convert` (convert a lead), available kwargs are (all optional):
  - person
  - company (`prosperworks.models.Company`)
  - opportunity


#### Examples:
```python
from prosperworks import api
from prosperworks.models import Company

api.configure('key', 'your.name@example.com')

new_co = Company.create(name='New Co.')
print new_co.id

lead = Lead.create(name='John Doe')
lead.name = 'Jane Doe'
lead.update()
print lead.id

lead.convert(company=new_co)
```
