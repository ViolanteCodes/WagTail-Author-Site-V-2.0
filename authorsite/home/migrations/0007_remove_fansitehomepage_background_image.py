# Generated by Django 3.0.13 on 2021-03-22 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_fansitehomepage_background_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fansitehomepage',
            name='background_image',
        ),
    ]
