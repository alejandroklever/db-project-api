# Generated by Django 3.1 on 2020-08-16 17:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('revista_cientifica', '0017_auto_20200815_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='articleinreview',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='file',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]