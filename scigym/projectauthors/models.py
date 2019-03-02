import logging

from django.db import models
from django.contrib.postgres.fields import JSONField

from scigym.config.models import Base

logger = logging.getLogger('django')

class ProjectAuthor(Base):
    # fields based on github API
    # TODO which fields are not private?
    github_id = models.PositiveIntegerField()
    login = models.CharField(max_length=256)  # TODO what is the actual max length?
    html_url = models.URLField()
    avatar_url = models.URLField()

    # fields not based on github API
    full_name = models.CharField(max_length=256)
