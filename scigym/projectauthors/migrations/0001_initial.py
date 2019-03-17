# Generated by Django 2.1.7 on 2019-02-27 17:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAuthor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('github_id', models.PositiveIntegerField()),
                ('login', models.CharField(max_length=256)),
                ('html_url', models.URLField()),
                ('avatar_url', models.URLField()),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]