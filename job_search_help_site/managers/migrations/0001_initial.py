# Generated by Django 4.2.3 on 2024-01-24 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('search_site', '0019_requesttoverificationuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationUserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_confirm', models.DateTimeField(default=None, null=True, verbose_name='Date of confirm request')),
                ('confirm', models.BooleanField(default=False, verbose_name='Confirm of request')),
                ('manager', models.OneToOneField(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('request_verification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_site.requesttoverificationuser')),
            ],
            options={
                'verbose_name_plural': 'Потверждение верификации роли пользователя',
                'ordering': ['-date_confirm'],
            },
        ),
    ]