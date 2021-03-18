from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from puput.abstracts import BlogAbstract

class MyBlogAbstract(BlogAbstract):
    """Puput Base Blog Abstract model, extended to allow for custom methods
    and template choices."""
    # Template choices change the template that will be extended. Template
    # path/name goes in left side of tuple, human readable name on right!
    TEMPLATE_CHOICES = [
        ('base_dark.html', 'Dark'),
        ('Light_Theme', 'Light')
    ]
    template_theme = models.CharField(
        max_length = 250,
        choices = TEMPLATE_CHOICES,
        default = 'Dark', 
        help_text = """
        Choose dark theme to match main site and light theme
        to match light site."""
    )
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    pinterest_url = models.URLField(blank=True)

    # Note that header image and color picker are no longer included in 
    # content panels. These are normally
    # included in the puput blog page but in this case, we don't want to 
    # disrupt the custom themes!
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
        # Get template_theme from model and pass to context as 'template_theme'
        context['template_theme'] = self.template_theme
        return context
