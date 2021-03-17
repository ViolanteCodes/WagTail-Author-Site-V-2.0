# Generated by Django 3.0.13 on 2021-03-16 19:35

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('book_title', models.CharField(help_text='The exact title of the book. It will \n    be saved in this format in the database to display on related pages.', max_length=200)),
                ('release_date', models.DateField(blank=True, help_text='The book release date. This\n    field is optional.', null=True)),
                ('teaser', models.TextField(blank=True, help_text='A brief teaser description of your \n    book. This is the paragraph that will show up on the "all books" page.', null=True)),
                ('description', wagtail.core.fields.RichTextField(blank=True, help_text='A description of your book.', null=True)),
                ('other_text', wagtail.core.fields.RichTextField(blank=True, help_text='This is an optional field. Text\n    added and formatted here will appear close to the bottom of the book page, right above the section\n    for content warnings.', null=True)),
                ('sort_order', models.IntegerField(blank=True, help_text='This field is optional, but if filled in,\n    it lets you pick where this book shows up in the "all books" section of your website. The higher the number, the \n    closer to the top of the page the book will be.', null=True)),
                ('author', models.ForeignKey(blank=True, help_text="Choose one of your Author Pages to assign a pen name to this book. \n        If you don't see the pen name you want, you might need to set up a new AuthorPage \n        for that pen name!", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BooksIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('repeat_in_subnav', models.BooleanField(default=False, help_text="If checked, a link to this page will be repeated alongside it's direct children when displaying a sub-navigation for this page.", verbose_name='repeat in sub-navigation')),
                ('repeated_item_text', models.CharField(blank=True, help_text="e.g. 'Section home' or 'Overview'. If left blank, the page title will be used.", max_length=255, verbose_name='repeated item link text')),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='ContentWarning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SeriesPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('series_name', models.CharField(max_length=200)),
                ('total_books', models.IntegerField()),
                ('series_description', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BookPageReviewBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('reviewer', models.CharField(blank=True, max_length=255)),
                ('review_venue', models.CharField(blank=True, max_length=255)),
                ('review_text', models.TextField(blank=True)),
                ('review_link', models.URLField(blank=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_reviews', to='books.BookPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookPageBuyLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('vendor_name', models.CharField(max_length=255)),
                ('link_address', models.URLField(blank=True, verbose_name='URL')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_links', to='books.BookPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bookpage',
            name='content_warnings',
            field=models.ManyToManyField(blank=True, help_text='(Optional):\n    Choose one or more content warnings for this book. If you don\'t see the warning you want listed here,\n    click "Add Content Warnings on the menu on the left and add in your warnings.', to='books.ContentWarning'),
        ),
        migrations.AddField(
            model_name='bookpage',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='bookpage',
            name='genre',
            field=models.ManyToManyField(blank=True, help_text='Optional: Choose one or more\n    genres for this book. If you don\'t see the genre you need, click "Add Genre to List" from the menu\n    on the left and add in your genre.', to='books.Genre'),
        ),
        migrations.AddField(
            model_name='bookpage',
            name='series',
            field=models.ForeignKey(blank=True, help_text="Choose a series page to assign this book to a Series. If you don't see\n        the series you want, you might need to set up a new Series Page.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.CreateModel(
            name='AuthorPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('author_pen_name', models.CharField(max_length=200)),
                ('author_bio', wagtail.core.fields.RichTextField()),
                ('author_photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
