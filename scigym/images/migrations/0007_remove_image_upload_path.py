# Generated by Django 2.1.7 on 2019-10-06 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_image_upload_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='upload_path',
        ),
    ]
