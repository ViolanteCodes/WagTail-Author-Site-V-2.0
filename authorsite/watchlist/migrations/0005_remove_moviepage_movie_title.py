# Generated by Django 3.0.13 on 2021-03-23 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0004_moviepage_release_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviepage',
            name='movie_title',
        ),
    ]
