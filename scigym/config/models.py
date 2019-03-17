import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

from scigym.users.models import User

IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg']

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug


class ConfigManager(models.Manager):
    def load(self):
        config, created = self.get_or_create(pk=1)
        return config

class ImageConfig(models.Model):
    valid_image_formats = ArrayField(models.CharField(max_length=10), default=list) #this should be a initial default

    objects = ConfigManager()

    def __str__(self):
        return 'Image configuration'

    def delete(self, *args, **kwargs):
        return NotImplementedError('The image configuration cannot be deleted')

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
