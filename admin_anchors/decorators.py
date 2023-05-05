from django.core.exceptions import ImproperlyConfigured
from django.contrib import admin
from django.db import models

from admin_anchors.utils import (
    create_admin_anchor,
    resolve_instance_field_path,
)


def admin_anchor(dotted_field_path: str):
    def inner(func):
        def wrapper(model_admin: admin.ModelAdmin, instance: models.Model) -> str:
            field_path = dotted_field_path.split(".")
            field_name = field_path.pop()

            field_parent_path = field_path
            field_parent = resolve_instance_field_path(instance, field_parent_path)

            if field_parent is None:
                return model_admin.get_empty_value_display()

            field = field_parent._meta.get_field(field_name)
            related_model = field.related_model

            if related_model is None:
                raise ImproperlyConfigured(f"Non-relation field referenced: {field}")

            args = None
            query = None

            if isinstance(field, (models.OneToOneRel, models.ForeignKey)):
                field_value = getattr(field_parent, field_name, None)
                if not field_value:
                    return model_admin.get_empty_value_display()
                args = [field_value.id]
            elif isinstance(field, (models.ManyToOneRel, models.ManyToManyRel)):
                query = {f"{field.field.name}__id": instance.pk}
            elif isinstance(field, models.ManyToManyField):
                query = {f"{field.related_query_name()}__id": instance.pk}

            page_name = "change" if args else "changelist"

            return create_admin_anchor(
                page_name=page_name,
                app_label=related_model._meta.app_label,
                model_name=related_model._meta.model_name,
                label=func(model_admin, instance),
                args=args,
                query=query,
            )

        wrapper.__name__ = func.__name__
        return wrapper

    return inner
