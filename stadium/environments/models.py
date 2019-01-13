from django.db import models

from stadium.config.models import Base
from stadium.users.models import User
from stadium.repositories.models import Repository
from django.contrib.postgres.fields import ArrayField


class Environment(Base):
  
    repository = models.OneToOneField(Repository, on_delete=models.CASCADE)

    # new as compared to repo model
    
    name = models.CharField(max_length=256) # TODO what is the actual max length?
    description = models.TextField(blank=True, default='', null=True)
    # image = models.TextField(blank=True, null=True) # TODO add this field
    tags = ArrayField(models.CharField(max_length=50), size=4, null=True)
