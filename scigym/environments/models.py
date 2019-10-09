from django.db import models
from django.core.validators import RegexValidator

from scigym.config.models import Base
from scigym.users.models import User
from scigym.repositories.models import Repository
from scigym.images.models import Image
from django.contrib.postgres.fields import ArrayField


class Environment(Base):

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z- ]*$', 'Only alphanumeric characters are allowed.')
  
    repository = models.OneToOneField(Repository, on_delete=models.CASCADE)

    # new as compared to repo model
    
    name = models.CharField(max_length=256, unique=True, validators=[alphanumeric]) # TODO what is the actual max length?
    url = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, default='', null=True)
    scigym = models.BooleanField(default=False) # only we can edit this field
    tags = ArrayField(models.CharField(max_length=50), size=4, null=True)
    topic = models.ForeignKey('Topic', null=True, on_delete=models.SET_NULL)
    current_avatar = models.ForeignKey(Image, null=True, on_delete=models.SET_NULL)


class Topic(Base):

    name = models.CharField(max_length=100, unique=True, blank=False)
    parent_topic = models.ForeignKey('Topic', null=True, on_delete=models.SET_NULL, blank=True)
