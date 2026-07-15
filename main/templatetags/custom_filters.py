import re

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def urlize_custom(text):
    url_pattern = re.compile(r"(https?://[^\s]+)")

    def replace_url(match):
        url = match.group(0)
        return (
            f'<a class="text-blue-500 break-all" href="{url}" '
            f'target="_blank" rel="noopener noreferrer">{url}</a>'
        )

    return mark_safe(url_pattern.sub(replace_url, text or ""))
