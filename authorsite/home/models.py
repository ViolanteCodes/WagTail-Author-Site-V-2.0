from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from django.conf import settings
from wagtail.contrib.settings.models import BaseSetting, register_setting

class HomePage(Page):
    """A stylish, custom landing page with hero image background and book image."""
    background_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    book_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    caption_text = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('background_image'),
        ImageChooserPanel('book_image'),
        FieldPanel('caption_text', classname="full"),
    ]

@register_setting
class SocialMediaSettings(BaseSetting):
    """Social media settings, will show up in menu."""
    facebook = models.URLField(
        help_text='Your Facebook page URL')
    instagram = models.URLField(
        help_text='Your Instagram URL')
    twitter = models.URLField(
        help_text='Your Twitter URL')