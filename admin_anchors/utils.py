from typing import Any

from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode


def get_field(model: type[models.Model], field_name: str):
    """
    Look up a field by name, falling back to reverse relation accessor names.

    Reverse relations are named after their related query name (e.g. "user"),
    but are accessed on instances through their accessor name, which defaults
    to "<model>_set" (e.g. "user_set") when no related_name is given.
    """
    try:
        return model._meta.get_field(field_name)
    except FieldDoesNotExist:
        for related_object in model._meta.related_objects:
            if related_object.get_accessor_name() == field_name:
                return related_object
        raise


def get_field_accessor_name(field) -> str:
    if isinstance(field, models.ForeignObjectRel):
        return field.get_accessor_name()
    return field.name


def resolve_instance_field_path(
    instance: models.Model, field_path: list[str]
) -> models.Model | None:
    if not field_path:
        return instance

    field_name = field_path.pop(0)

    try:
        next_instance = getattr(instance, field_name)
    except ObjectDoesNotExist:
        return None

    return resolve_instance_field_path(next_instance, field_path)


def create_admin_anchor(
    app_label: str,
    model_name: str,
    label: str,
    query: dict[str, Any],
) -> str:
    path = reverse(f"admin:{app_label}_{model_name}_changelist")
    query_string = urlencode(query)
    url = f"{path}?{query_string}"
    return format_html("<a href='{}'>{}</a>", url, label)
