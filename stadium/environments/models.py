import logging

from django.db import models
from django.contrib.postgres.fields import JSONField

from stadium.config.models import Base
from stadium.users.models import User


logger = logging.getLogger('django')


class Repository(Base):
    # fields exact same as github API JSON
    name = models.CharField(max_length=256)  # TODO what is the actual max length?
    full_name = models.CharField(max_length=256)  # TODO what is the actual max length?
    homepage = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True, default='')
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

    class Meta:
        verbose_name_plural = 'repositories'


class Environment(Base):
    """
    represents a Github repository that contains a pypi gym environment
    """
    # TODO - chronjob to refresh repo information
    # TODO - allow user to manually refresh information

    # fields not from github at all that we have to derive
    pypi_url = models.URLField(null=True, blank=True)
    pypi_name = models.CharField(max_length=256)
    repository = models.ForeignKey(Repository, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256)
    public = models.BooleanField(default=True)
