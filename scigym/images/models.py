import logging

from django.db import models

from scigym.config.models import Base
from scigym.users.models import User

class Image(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    file_path = models.TextField()
    hash = models.CharField(max_length=255, null=False)

class ImageUploadEvent(Base):
    file_name = models.CharField(max_length=255)
    image = models.ManyToManyField(Image)
    description = models.TextField(default='')
