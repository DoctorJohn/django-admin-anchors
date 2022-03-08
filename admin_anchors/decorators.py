from django.core.exceptions import ImproperlyConfigured
from django.db import models

from admin_anchors.utils import (
    create_admin_anchor,
    get_selected_field,
    get_selected_obj,
)


def admin_anchor(selector: str):
    def inner(func):
        def wrapper(self, instance) -> str:
            obj = get_selected_obj(instance, selector)

            if obj is None:
                return self.get_empty_value_display()

            field = get_selected_field(instance, selector)
            related_model = field.related_model
            args = None
            query = None

            if isinstance(field, (models.OneToOneRel, models.ForeignKey)):
                field_value = getattr(obj, field.name, None)
                if not field_value:
                    return self.get_empty_value_display()
                args = [field_value.id]

            elif isinstance(field, (models.ManyToOneRel, models.ManyToManyRel)):
                query = {f"{field.field.name}__id": instance.id}

            elif isinstance(field, models.ManyToManyField):
                query = {f"{field.related_query_name()}__id": instance.id}

            else:
                raise ImproperlyConfigured(f"Non-relation field referenced: {field}")

            page_name = "change" if args else "changelist"

            return create_admin_anchor(
                page_name=page_name,
                app_label=related_model._meta.app_label,
                model_name=related_model._meta.model_name,
                label=func(self, instance),
                args=args,
                query=query,
            )

        wrapper.__name__ = func.__name__
        return wrapper

    return inner
