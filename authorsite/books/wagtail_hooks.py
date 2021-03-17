"""
Hooks to expose Django Genre and Content Warning Models to Model Admin
"""

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, 
    ModelAdminGroup, 
    modeladmin_register 
)
from .models import Genre, ContentWarning

class GenreAdmin(ModelAdmin):
    """Custom Admin Menu Item for Genres"""
    model = Genre
    menu_label = "Add Genre to List"
    menu_icon = "edit"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display=('name',)

class ContentWarningAdmin(ModelAdmin):
    """Custom Admin Menu item for Content Warnings"""
    model = ContentWarning
    menu_label = "Add Content Warnings"
    menu_icon = 'edit'
    menu_order = 501
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display=('name',)

modeladmin_register(GenreAdmin)
modeladmin_register(ContentWarningAdmin)