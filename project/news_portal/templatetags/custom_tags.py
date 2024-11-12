from datetime import datetime

from django import template


register = template.Library()


@register.simple_tag()
def current_time(time=datetime, format_string='%d %B %Y'):
   return time.utcnow().strftime(format_string)
