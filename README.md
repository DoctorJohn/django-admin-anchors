# Django Admin Anchors

[![PyPI][pypi-image]][pypi-url]
[![License][license-image]][license-url]
[![Tests][tests-image]][tests-url]

[pypi-image]: https://img.shields.io/pypi/v/django-admin-anchors
[pypi-url]: https://pypi.org/project/django-admin-anchors/
[license-image]: https://img.shields.io/pypi/l/django-admin-anchors
[license-url]: https://github.com/DoctorJohn/django-admin-anchors/blob/master/LICENSE
[tests-image]: https://github.com/DoctorJohn/django-admin-anchors/workflows/Tests/badge.svg
[tests-url]: https://github.com/DoctorJohn/django-admin-anchors/actions

Turn Django admin list display items into clickable links to related objects using
decorators.

## Installation

`pip install django-admin-anchors`

## Usage

Take a look at the `tests/project` directory to see a runnable example project.

### Add links to the object list page

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

### Add links to the object edit page

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
