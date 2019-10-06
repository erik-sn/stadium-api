import logging

from django.db import models
from django.contrib.postgres.fields import JSONField

from scigym.config.models import Base

logger = logging.getLogger('django')

# CONTRIBUTION_CHOICES = (
#     ('web', 'web'),
#     ('package', 'package'),
# )

class Contributor(Base):
    # fields based on github API JSON https://api.github.com/repos/hendrikpn/scigym-web/stats/contributors
    # TODO which fields are not private?
    github_id = models.PositiveIntegerField()
    login = models.CharField(max_length=256)  # TODO what is the actual max length?
    html_url = models.URLField()
    avatar_url = models.URLField()
    contributions = models.PositiveIntegerField()

    # fields not based on github API
    # contributed_to = models.CharField(choices=CONTRIBUTION_CHOICES) # maybe separate web and package in the future

    class Meta:
        abstract = False
        ordering = ('-contributions',)
