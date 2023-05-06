from typing import Dict, List, Optional, Any

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
    app_label: str,
    model_name: str,
    label: str,
    query: Dict[str, Any],
) -> str:
    path = reverse(f"admin:{app_label}_{model_name}_changelist")
    query_string = urlencode(query)
    url = f"{path}?{query_string}"
    return format_html("<a href='{}'>{}</a>", url, label)
