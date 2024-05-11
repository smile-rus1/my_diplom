# Generated by Django 4.2.3 on 2023-08-24 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search_site', '0009_delete_application'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(default='', max_length=30, verbose_name='Название компании')),
                ('application_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата отклика')),
                ('cover_letter', models.TextField(null=True, verbose_name='Сопроводительное письмо')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_site.applicant', verbose_name='Кандидат')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_site.vacancy', verbose_name='Вакансия')),
            ],
            options={
                'verbose_name_plural': 'Отправка резюме',
            },
        ),
    ]