# Prosperworks Api
A python based api wrapper for [Prosperworks](https://www.prosperworks.com/developer_api).

# Models
### `prosperworks.models.Company`
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

#### Examples:
```python
from prosperworks import api, utils
from prosperworks.models import Company

api.configure('key', 'your.name@example.com')
for company in Company.search():
    print company.name
```
