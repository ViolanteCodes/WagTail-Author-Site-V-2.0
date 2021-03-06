from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from django.conf import settings
from wagtail.contrib.settings.models import BaseSetting, register_setting

class HomePage(Page):
    """A stylish, custom landing page with hero image background and book image."""
    author_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    book_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    background_image =  models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name="+", null=True)
    caption_text = models.CharField(blank=True, null=True, max_length=250)
    book_link_page = models.ForeignKey(
        'books.BookPage', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Optional field: if you'd like your main book image to link to a book page, 
        choose that page here.""")

    content_panels = Page.content_panels + [
        ImageChooserPanel('author_image'),
        ImageChooserPanel('book_image'),
        ImageChooserPanel('background_image'),
        FieldPanel('caption_text', classname="full"),
        PageChooserPanel('book_link_page'),
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

    content_panels = Page.content_panels + [
        FieldPanel('w_page', classname="full"),
        FieldPanel('a_page', classname="full"),
        FieldPanel('r_page', classname="full"),
        FieldPanel('d_page', classname="full"),
        FieldPanel('e_page', classname="full"),
        FieldPanel('n_page', classname="full"),
    ]

    subpage_types = ['puput.BlogPage','contact.ContactPage', 'watchlist.MovieIndexPage', 'watchlist.DossierPage', 'watchlist.ArmoryIndexPage']

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
    tiktok = models.URLField(
        help_text="Your TikTok URL", blank=True, null=True)

