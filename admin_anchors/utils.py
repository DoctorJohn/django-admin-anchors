from typing import Optional, Dict, List
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
