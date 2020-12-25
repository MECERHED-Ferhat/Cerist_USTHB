from django import template
import time

register = template.Library()

@register.simple_tag
def current_time():
	return str(time.time())