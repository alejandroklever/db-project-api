# Generated by Django 3.1 on 2020-08-15 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revista_cientifica', '0013_remove_notification_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='checked',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]