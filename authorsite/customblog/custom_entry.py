from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from customblog.models import MyBlogAbstract
from puput.models import EntryPage, BlogPage

class CustomEntryPage(EntryPage):
    """An extended version of the entry page, using multi-table inheritance."""
    TEMPLATE_CHOICES = [
        ('base_dark.html', 'Dark'),
        ('base_light.html', 'Light')
    ]
    template_theme = models.CharField(
        max_length = 250,
        choices = TEMPLATE_CHOICES,
        default = 'Dark', 
        help_text = """
        Choose dark theme to match main site and light theme
        to match light site."""
    )

    content_panels = EntryPage.content_panels + [
        FieldPanel('template_theme'),
    ]

    MyBlogAbstract.subpage_types.append(CustomEntryPage)

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['entries'] = self.entries
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        context['template_theme'] = self.template_theme
        return context
