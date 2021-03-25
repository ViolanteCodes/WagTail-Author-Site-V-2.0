from django.db import models
from django.shortcuts import render
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.search import index
from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel

# Create your models here
class DossierPage(Page):
    """Home Page for the Dossier Entries"""
    character_page = models.ForeignKey(
        'watchlist.CharacterIndexPage', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose the character index page.""")
    producer_page = models.ForeignKey(
        'watchlist.ProducerIndexPage', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose the character index page.""")
    actor_page = models.ForeignKey(
        'watchlist.ActorIndexPage', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose the character index page.""")
    description = RichTextField()

    content_panels = Page.content_panels + [
            PageChooserPanel('character_page'),
            PageChooserPanel('producer_page'),
            PageChooserPanel('actor_page'),
            FieldPanel('description')
        ]

    parent_page_types = ['home.FanSiteHomePage']
    subpage_types = ['watchlist.CharacterIndexPage', 'watchlist.ProducerIndexPage', 'watchlist.ActorIndexPage']

class ProducerIndexPage(Page):
    """List of All Producers."""
    description = RichTextField()

    content_panels = Page.content_panels + [
            FieldPanel('description', classname="full"),
        ]

    parent_page_types = ['watchlist.DossierPage']
    subpage_types = ['watchlist.ProducerPage']

    def get_all_producers(self):
        """A custom method to return all producers from the database."""
        all_producers = ProducerPage.objects.order_by('title')
        return all_producers


class ActorIndexPage(Page):
    """List of all Actors."""
    description = RichTextField()

    content_panels = Page.content_panels + [
            FieldPanel('description', classname="full"),
        ]

    parent_page_types = ['watchlist.DossierPage']
    subpage_types = ['watchlist.ActorPage']

class MovieIndexPage(Page):
    """List of all Movies."""
    description = RichTextField()

    content_panels = Page.content_panels + [
            FieldPanel('description', classname="full"),
        ]

    parent_page_types = ['home.FanSiteHomePage']
    subpage_types = ['watchlist.MoviePage']

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        movie_pages = MoviePage.objects.order_by('film_number')
        context['movie_pages'] = movie_pages
        return context

class CharacterIndexPage(Page):
    """List of all Characters."""
    description = RichTextField()

    content_panels = Page.content_panels + [
            FieldPanel('description', classname="full"),
        ]
    parent_page_types = ['watchlist.DossierPage']
    subpage_types = ['watchlist.CharacterPage']

class ProducerPage(Page):
    """A model of a producer."""
    producer_bio = RichTextField()
    content_panels = Page.content_panels + [
            FieldPanel('producer_bio'),
        ]
        # Parent page / subpage type rules
    parent_page_types = ['watchlist.ProducerIndexPage']

    def get_produced_movies(self):
        """Custom method that returns titles and links for all 
        movies produced by this producer."""
        
        all_movies = MoviePage.objects.filter(producer=self).order_by('film_number')
        return all_movies


class ActorPage(Page):
    """A model of an actor."""
    actor_bio = RichTextField()

    content_panels = Page.content_panels + [
            FieldPanel('actor_bio'),
        ]
        # Parent page / subpage type rules
    parent_page_types = ['watchlist.ActorIndexPage']

class MoviePage(Page):
    """A page representing a movie entry."""
    film_number = models.IntegerField()
    release_year = models.IntegerField()
    producer = models.ForeignKey(
        'watchlist.ProducerPage', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose a producer. If you don't see your producer listed here, 
        it's probably because you didn't make the Producer Page yet!""")
    jove_brand_actor = models.ForeignKey(
        'watchlist.ActorPage', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose the actor that plays Jove Brand. If you don't see your actor listed here, 
        it's probably because you didn't make the Actor Page yet!""")
    rating = models.DecimalField(
        max_digits = 4, decimal_places = 1, blank=True, null=True, help_text="""
        Enter in a rating for this movie. Note: Can enter up to a tens place, e.g, 4.5."""
    )
    movie_description = RichTextField(help_text = """Describe the movie.""")

    content_panels = Page.content_panels + [
            FieldPanel('film_number'),
            FieldPanel('release_year'),
            PageChooserPanel('producer'),
            PageChooserPanel('jove_brand_actor'),
            FieldPanel('rating'),
            FieldPanel('movie_description'),
        ]
        # Parent page / subpage type rules
    parent_page_types = ['watchlist.MovieIndexPage']

class CharacterPage(Page):
    """A page representing a character entry."""
    character_name = models.CharField(max_length=250)
    character_description = RichTextField()

    content_panels = Page.content_panels + [
            FieldPanel('character_name'),
            FieldPanel('character_description', classname="full"),
        ]
        # Parent page / subpage type rules
    parent_page_types = ['watchlist.CharacterIndexPage']
