from django.db import models

from stadium.config.models import Base
from stadium.users.models import User
from stadium.repositories.models import Repository


class Environment(Base):
  
    repository = models.OneToOneField(Repository, on_delete=models.CASCADE)

    # new as compared to repo model
    
    name = models.CharField(max_length=256) # TODO what is the actual max length?
    description = models.TextField(blank=True, default='', null=True)
    # image = models.TextField(blank=True, null=True) # TODO add this field
    # tags = models.CharField(max_length=100) # TODO add this field