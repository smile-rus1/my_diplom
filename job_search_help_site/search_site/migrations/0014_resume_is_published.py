# Generated by Django 4.2.3 on 2023-09-18 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_site', '0013_application_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Опубликовано'),
        ),
    ]
