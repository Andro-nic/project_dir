from datetime import datetime

from django import template


register = template.Library()


@register.simple_tag()
def current_time(time=datetime, format_string='%d %B %Y'):
   return time.utcnow().strftime(format_string)

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()