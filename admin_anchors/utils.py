from typing import Optional, Dict, List
from django.db.models.fields import Field
from django.db import models
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html


def create_admin_anchor(
    page_name: str,
    app_label: str,
    model_name: str,
    label: str,
    args: Optional[List] = None,
    query: Optional[Dict] = None,
) -> str:
    url = reverse(f"admin:{app_label}_{model_name}_{page_name}", args=args)
    if query:
        url += "?" + urlencode(query)
    return format_html("<a href='{}'>{}</a>", url, label)


def get_selected_obj(instance: models.Model, selector: str) -> Optional[models.Model]:
    current = instance
    # The last part is the selected field
    parts = selector.split(".")[0:-1]
    for part in parts:
        current = getattr(current, part, None)
        if current is None:
            return None
    return current


def get_selected_field(instance: models.Model, selector: str) -> Optional[Field]:
    selection = get_selected_obj(instance, selector)
    if selection is None:
        return None
    field_name = selector.split(".")[-1]
    return selection._meta.get_field(field_name)
