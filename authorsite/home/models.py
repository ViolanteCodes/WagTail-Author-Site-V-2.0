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

class FanSiteHomePage(Page):
    """FanSite HomePage"""
    w_page = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose a page to assign to 'W' value.""")
    a_page = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose a page to assign to 'A' value.""")
    r_page = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose a page to assign to 'R' value.""")
    d_page = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose a page to assign to 'D' value.""")
    e_page = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose a page to assign to 'E' value.""")
    n_page = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose a page to assign to 'N' value.""")
    background_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)

    content_panels = Page.content_panels + [
        FieldPanel('w_page', classname="full"),
        FieldPanel('a_page', classname="full"),
        FieldPanel('r_page', classname="full"),
        FieldPanel('d_page', classname="full"),
        FieldPanel('e_page', classname="full"),
        FieldPanel('n_page', classname="full"),
        ImageChooserPanel('background_image'),
    ]

    subpage_types = ['puput.BlogPage','contact.ContactPage', 'watchlist.MovieIndexPage', 'watchlist.DossierPage']

    def get_context(self, request):
        """Custom context to create list of warden_pages."""
        context = super().get_context(request)
        # Add extra variables and return the updated context
        context['warden_pages'] = [
            self.w_page,
            self.a_page,
            self.r_page,
            self.d_page,
            self.e_page,
            self.n_page,
        ]
        return context

@register_setting
class SocialMediaSettings(BaseSetting):
    """Social media settings, will show up in menu."""
    facebook = models.URLField(
        help_text='Your Facebook page URL')
    instagram = models.URLField(
        help_text='Your Instagram URL')
    twitter = models.URLField(
        help_text='Your Twitter URL')