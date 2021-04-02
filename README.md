# Django Admin Anchors

Turn Django admin list display items into clickable links to related objects using
decorators.

## Installation

`pip install django-admin-anchors`

## Usage

```python
# yourapp/admin.py
from django.contrib import admin
from admin_anchors.decorators import admin_anchor
from yourapp.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "profile_link", "teams_link"]

    @admin_anchor(field_name="profile")
    def profile_link(self, instance):
        return "Profile"

    @admin_anchor(field_name="teams")
    def teams_link(self, instance):
        return f"{instance.teams.count()} teams"
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
