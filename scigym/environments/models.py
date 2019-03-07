from django.db import models

from scigym.config.models import Base
from scigym.users.models import User
from scigym.repositories.models import Repository
from scigym.images.models import Image
from django.contrib.postgres.fields import ArrayField


class Environment(Base):
  
    repository = models.OneToOneField(Repository, on_delete=models.CASCADE)

    # new as compared to repo model
    
    name = models.CharField(max_length=256) # TODO what is the actual max length?
    description = models.TextField(blank=True, default='', null=True)
    tags = ArrayField(models.CharField(max_length=50), size=4, null=True)
    topic = models.ForeignKey('Topic', null=True, on_delete=models.SET_NULL)

    # TODO: avatar: ManyToMany
    #       environment delete method, should also delete the images
    ##       maybe the ForeignKey should be on the image model
    ##       advantage: `on_delete=models.CASCADE`
    #       change: UPLOADED_STATIC_FILES, SAVED_IMAGES,
    #       change in image upload: last updated so that frontend gets the most up-to-date 
    #       special case: twice the same image -> hash should involve environmentID
    #       rename Image model to avatar, and save to avatar file system
    avatar = models.ManyToManyField(Image) 

class Topic(Base):

    name = models.CharField(max_length=100, unique=True, blank=False)
    parent_topic = models.ForeignKey('Topic', null=True, on_delete=models.SET_NULL, blank=True)
