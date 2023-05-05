from typing import Dict, List, Optional

from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.core.exceptions import ObjectDoesNotExist


def resolve_instance_field_path(
    instance: models.Model, field_path: List[str]
) -> Optional[models.Model]:
    if not field_path:
        return instance

    field_name = field_path.pop(0)

    try:
        next_instance = getattr(instance, field_name)
    except ObjectDoesNotExist:
        return None

    return resolve_instance_field_path(next_instance, field_path)


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
