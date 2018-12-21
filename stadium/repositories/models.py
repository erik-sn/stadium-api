import logging

from django.db import models
from django.contrib.postgres.fields import JSONField

from stadium.config.models import Base
from stadium.users.models import User


logger = logging.getLogger('django')


class Repository(Base):
    # fields exact same as github API JSON
    # TODO which fields are not private?
    name = models.CharField(max_length=256)  # TODO what is the actual max length?
    full_name = models.CharField(max_length=256)  # TODO what is the actual max length?
    homepage = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True, default='', null=True)
    private = models.BooleanField()
    fork = models.BooleanField()
    size = models.PositiveIntegerField()  # TODO what is this?
    stargazers_count = models.PositiveIntegerField()
    forks = models.PositiveIntegerField()
    watchers = models.PositiveIntegerField()
    html_url = models.URLField()
    ssh_url = models.URLField()
    git_url = models.URLField()
    raw_api_response = JSONField()

    # fields based on github API but not included in exact form as response JSON
    github_id = models.PositiveIntegerField()
    api_url = models.URLField()
    license = models.CharField(max_length=256, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    readme = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=True)
    pypi_name = models.CharField(max_length=256, null=True, blank=True)

    # fields not based on github API
    gym = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'repositories'

