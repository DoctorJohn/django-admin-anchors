# Django Admin Anchors

[![PyPI](https://img.shields.io/pypi/v/django-admin-anchors)](https://pypi.org/project/django-admin-anchors/)
[![PyPI - License](https://img.shields.io/pypi/l/django-admin-anchors)](https://github.com/DoctorJohn/django-admin-anchors/blob/master/LICENSE)

Turn Django admin list display items into clickable links to related objects using
decorators.

## Installation

`pip install django-admin-anchors`

## Usage

```python
from django.contrib import admin
from admin_anchors import admin_anchor
from yourapp.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["__str__", "captain_link", "captains_profile_link", "members_link"]

    @admin_anchor(field_name="captain")
    def captain_link(self, instance):
        return str(instance.captain)

    @admin_anchor(field_name="captain.profile")
    def captains_profile_link(self, instance):
        return "Captains profile"

    @admin_anchor(field_name="members")
    def members_link(self, instance):
        return f"{instance.members.count()} members"
```

Take a look at the `tests/project` directory to see a runnable example project.

## Contributing

### Setup

1. Clone the repository and enter the cloned folder
2. (optional) Create and activate a dedicated Python virtual environment
3. Run `pip install -e ".[dev]"` to install the projects requirements
4. (optional) Run `pre-commit install` to install the pre-commit hook

### Pre-commit hook

Our pre-commit hook formats and lints the code.

### Formatting and linting

- Run `black admin_anchors tests` to format the code
- Run `flake8 admin_anchors tests` to lint the code

### Testing

- Run `py.test --cov admin_anchors tests` to run the tests in the current Python env
- Run `tox` to run the tests in all supported Python and Django environments

### Makefile

All commands listed above have shortcut make recipes.
Take a look at the `Makefile` to learn more.
