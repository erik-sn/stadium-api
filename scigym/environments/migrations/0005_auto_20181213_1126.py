# Generated by Django 2.1.3 on 2018-12-13 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('environments', '0004_auto_20181213_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='repository',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repositories.Repository'),
        ),
    ]
