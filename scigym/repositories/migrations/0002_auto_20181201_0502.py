# Generated by Django 2.1.3 on 2018-12-01 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='pypi_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]