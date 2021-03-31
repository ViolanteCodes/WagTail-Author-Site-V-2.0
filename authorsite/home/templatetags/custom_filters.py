# These next two lines are necessary for Django to recognize that 
# the following function calls are for custom filters.

from django import template
from django.conf import settings
register = template.Library()

# Custom filters go here.
@register.simple_tag
def get_site_name():
    """Simple tag to pull site name from settings."""
    site_name = settings.WAGTAIL_SITE_NAME
    return site_name

@register.simple_tag
def get_fansite_name():
    """Simple tag to pull fansite name from settings."""
    fansite_name = settings.WAGTAIL_FANSITE_NAME
    return fansite_name

@register.simple_tag
def get_font_awesome_url():
    """Simple tag to pull fontawesome url from settings."""
    font_awesome_url = settings.FONT_AWESOME_URL
    return font_awesome_url

@register.filter(name='split')
def split(listname, splitter):
    """
    Returns the value turned into a list.
    """
    return listname.split(splitter)
