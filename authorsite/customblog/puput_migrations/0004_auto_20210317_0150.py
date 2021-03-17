# Generated by Django 3.0.13 on 2021-03-17 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puput', '0003_blogpage_template_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='template_theme',
            field=models.CharField(choices=[('base_dark.html', 'Dark Theme'), ('Light_Theme', 'Light Theme')], default='Dark_Theme', max_length=250),
        ),
    ]
