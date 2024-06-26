# Generated by Django 4.2.3 on 2024-04-10 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='is_subscribe',
            field=models.BooleanField(default=True, verbose_name='Подписан на рассылку'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='date_subscribe',
            field=models.DateTimeField(auto_now=True, verbose_name='Время подписки на рассылку уведомления'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='role',
            field=models.CharField(choices=[('applicant', 'Applicant'), ('company', 'Employer')], max_length=20, verbose_name='Роль пользователя'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='type_notifications',
            field=models.ManyToManyField(to='notifications.typenotifications', verbose_name='Тип уведомления'),
        ),
    ]
