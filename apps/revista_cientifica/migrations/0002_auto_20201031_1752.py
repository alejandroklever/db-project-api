# Generated by Django 3.1.1 on 2020-10-31 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revista_cientifica', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='profile_image_url',
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='apps/revista_cientifica/media'),
        ),
    ]
