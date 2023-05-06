# Django Admin Anchors

[![PyPI][pypi-image]][pypi-url]
![PyPI - Python Version][python-image]
![PyPI - Django Version][django-image]
[![License][license-image]][license-url]
[![Tests][tests-image]][tests-url]

[pypi-image]: https://img.shields.io/pypi/v/django-admin-anchors
[pypi-url]: https://pypi.org/project/django-admin-anchors/
[python-image]: https://img.shields.io/pypi/pyversions/django-admin-anchors
[django-image]: https://img.shields.io/pypi/djversions/django-admin-anchors
[license-image]: https://img.shields.io/pypi/l/django-admin-anchors
[license-url]: https://github.com/DoctorJohn/django-admin-anchors/blob/master/LICENSE
[tests-image]: https://github.com/DoctorJohn/django-admin-anchors/workflows/Tests/badge.svg
[tests-url]: https://github.com/DoctorJohn/django-admin-anchors/actions

Turn Django admin list display items into clickable links to related
objects using decorators.

Clicking admin anchors will redirect to a filtered changelist view
showing the related objects. This allows you to get a quick overview
and run actions on the filtered objects.

## Installation

`pip install django-admin-anchors`

## Usage

Take a look at the `tests/project` directory to see a runnable example project.

### Add links to the object list page

![Object list page](.github/images/list.png)

```python
from django.contrib import admin
from admin_anchors import admin_anchor
from yourapp.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["__str__", "captain_link", "captains_profile_link", "members_link"]

    @admin_anchor("captain")
    def captain_link(self, instance):
        return str(instance.captain)

    @admin_anchor("captain.profile")
    def captains_profile_link(self, instance):
        return "Captains profile"

    @admin_anchor("members")
    def members_link(self, instance):
        return f"{instance.members.count()} members"
```

### Add links to the object update page

![Object change page](.github/images/change.png)

```python
from django.contrib import admin
from admin_anchors import admin_anchor
from yourapp.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    readonly_fields = ["profile_link"]

    @admin_anchor("profile")
    def profile_link(self, instance):
        return "Profile"
```

## Example project

Take a look at our Django example project under `tests/project`.
You can run it by executing these commands:

1. `poetry install`
2. `poetry run python tests/project/manage.py migrate`
3. `poetry run python tests/project/manage.py createsuperuser`
4. `poetry run python tests/project/manage.py runserver`
