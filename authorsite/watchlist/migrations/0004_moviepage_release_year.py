# Generated by Django 3.0.13 on 2021-03-23 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0003_remove_moviepage_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviepage',
            name='release_year',
            field=models.IntegerField(default=1996),
            preserve_default=False,
        ),
    ]