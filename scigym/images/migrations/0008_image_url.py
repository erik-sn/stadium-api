# Generated by Django 2.1.7 on 2019-10-08 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_remove_image_upload_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
