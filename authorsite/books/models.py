from django import forms
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.search import index
from django.utils.text import slugify  
from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel

# Create your models here.

class Genre(models.Model):
    """A representation of a genre."""
    name = models.CharField(max_length=200)

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.name) 
        super(Genre, self).save(*args, **kwargs) 

    def __str__(self):
        return self.name

class ContentWarning(models.Model):
    """A representatation of a content warning."""
    name = models.CharField(max_length=200)

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.name) 
        super(ContentWarning, self).save(*args, **kwargs) 

    def __str__(self):
        return self.name

class AuthorPage(Page):
    """A representation of an author's pen name."""
    author_pen_name = models.CharField(max_length=200)
    author_bio = RichTextField()
    author_photo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('author_pen_name'),
        FieldPanel('author_bio'),
        ImageChooserPanel('author_photo'),
    ]
    # Parent page / subpage type rules
    parent_page_types = ['books.BooksIndexPage']

class SeriesPage(Page):
    """A page to represent a book series."""
    series_name = models.CharField(max_length=200)
    total_books = models.IntegerField()
    series_description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('series_name'),
        FieldPanel('series_description'),
        FieldPanel('total_books'),
    ]
    # Parent page / subpage type rules

    parent_page_types = ['books.BooksIndexPage']

### The following models are displayed on the Books Page ###
# The ABSTRACT model for Buy Links, with panels

class BuyLink(models.Model):
    # An individual buy_link for a book.
    vendor_name = models.CharField(max_length=255)
    link_address = models.URLField("URL", blank=True)
    panels = [
        FieldPanel('vendor_name'),
        FieldPanel('link_address'),
    ]
    class Meta:
        abstract = True
# Set the item as keyed to the page.
class BookPageBuyLinks(Orderable, BuyLink):
    page = ParentalKey('books.BookPage', on_delete=models.CASCADE, related_name='buy_links')

# Abstract model for book reviews, with panels:
class BookReview(models.Model):
    reviewer = models.CharField(max_length=255, blank=True)
    review_venue = models.CharField(max_length=255, blank=True)
    review_text = models.TextField(blank=True)
    review_link = models.URLField(blank=True)
    panels = [
        FieldPanel('reviewer'),
        FieldPanel('review_venue'),
        FieldPanel('review_text', classname="full"),
        FieldPanel('review_link'),
    ]
    class Meta:
        abstract = True
class BookPageReviewBox(Orderable, BookReview):
    page = ParentalKey('books.BookPage', on_delete=models.CASCADE, related_name='book_reviews')

### Book Page ###
class BookPage(Page):
    """A page for an individual book."""
    book_title = models.CharField(max_length=200, help_text="""The exact title of the book. It will 
    be saved in this format in the database to display on related pages.""")
    author = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose one of your Author Pages to assign a pen name to this book. 
        If you don't see the pen name you want, you might need to set up a new AuthorPage 
        for that pen name!""")
    series = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', 
        help_text="""Choose a series page to assign this book to a Series. If you don't see
        the series you want, you might need to set up a new Series Page.""")
    release_date = models.DateField(blank=True, null=True, help_text="""The book release date. This
    field is optional.""")
    genre = models.ManyToManyField('books.Genre', blank=True, help_text = """Optional: Choose one or more
    genres for this book. If you don't see the genre you need, click "Add Genre to List" from the menu
    on the left and add in your genre.""")
    teaser = models.TextField(blank=True, null=True, help_text="""A brief teaser description of your 
    book. This is the paragraph that will show up on the "all books" page.""")
    description = RichTextField(blank=True, null=True, help_text="""A description of your book.""")
    content_warnings = models.ManyToManyField('books.ContentWarning', blank=True, help_text="""(Optional):
    Choose one or more content warnings for this book. If you don't see the warning you want listed here,
    click "Add Content Warnings on the menu on the left and add in your warnings.""")
    cover_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    other_text = RichTextField(blank=True, null=True, help_text="""This is an optional field. Text
    added and formatted here will appear close to the bottom of the book page, right above the section
    for content warnings.""")
    sort_order = models.IntegerField(null=True, blank=True, help_text="""This field is optional, but if filled in,
    it lets you pick where this book shows up in the "all books" section of your website. The higher the number, the 
    closer to the top of the page the book will be.""")
    # Add content panels
    content_panels = Page.content_panels + [
        FieldPanel('book_title', classname="full"),
        PageChooserPanel('author', 'books.AuthorPage'),
        PageChooserPanel('series', 'books.SeriesPage'),
        FieldPanel('release_date'),
        FieldPanel('genre'),
        FieldPanel('description', classname="full"),
        ImageChooserPanel('cover_image'),
        FieldPanel('sort_order'),
        FieldPanel('content_warnings'),
        FieldPanel('other_text'),
        InlinePanel('buy_links', label="Buy Links"),
        InlinePanel('book_reviews', label="Book Reviews"),
    ]
    # Parent page / subpage type rules
    parent_page_types = ['books.BooksIndexPage']

class BooksIndexPage(Page, MenuPageMixin):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        menupage_panel,
    ]
    
    def serve(self, request):
        """Custom serve method"""
        book_list = BookPage.objects.live().order_by('-sort_order')
        return render(request, 'books/books_index_page.html', {
            'page':self,
            'book_list':book_list
        })
