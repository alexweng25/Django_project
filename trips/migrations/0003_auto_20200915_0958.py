# Generated by Django 3.0.8 on 2020-09-15 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_auto_20200911_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='photo',
        ),
        migrations.AddField(
            model_name='photos',
            name='image',
            field=models.ImageField(blank=True, upload_to='photo'),
        ),
    ]
