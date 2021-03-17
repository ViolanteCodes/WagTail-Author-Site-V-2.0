from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from puput.abstracts import BlogAbstract


class MyBlogAbstract(BlogAbstract):
    """Puput Base Blog Abstract model, extended to allow for custom methods
    and template choices."""
    TEMPLATE_CHOICES = [
        ('base_dark.html', 'Dark Theme'),
        ('Light_Theme', 'Light Theme')
    ]
    template_theme = models.CharField(
        max_length = 250,
        choices = TEMPLATE_CHOICES,
        default = 'Dark_Theme', 
        help_text = """
        Choose dark theme to match main site and light theme
        to match light site."""
    )
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    pinterest_url = models.URLField(blank=True)

    # Remote header_image and color picker from content panels
    content_panels = [
        FieldPanel('description', classname="full"),
        FieldPanel('template_theme'),
    ]
    settings_panels = BlogAbstract.settings_panels + [MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('instagram_url'),
            FieldPanel('pinterest_url'),
        ], heading=_("Socials"))]

    class Meta:
        abstract = True

    def get_context(self, request, *args, **kwargs):
        context = super(MyBlogAbstract, self).get_context(request, *args, **kwargs)
        context['entries'] = self.entries
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        context['template_theme'] = self.template_theme
        return context
