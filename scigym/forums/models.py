from django.db import models
from django.contrib.postgres.fields import ArrayField

from scigym.config.models import Base
from scigym.users.models import User
from scigym.environments.models import Environment

class MessageBoard(Base):
    # Message Board style with stackoverflow in mind.
    # Each environment has many Commentary Boards where people can ask questions or comment on the environment.
    # Environments will receive board key.
    title = models.CharField(max_length=50, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # admin = models.ManyToMany(User, on_delete=models.SET_NULL) # TODO: this is the environment owner # is this redundant?
    description = models.TextField(max_length=30000) # TODO: can this be markdown style? or at least the stackoverflow style?
    # num_comments = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    # upvotes = models.PositiveSmallIntegerField(default=0, blank=True, null=True) # this should be a class because of user assoc
    tags = ArrayField(models.CharField(max_length=50), size=4, null=True)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, null=True)

class Comment(Base):
    comment = models.TextField(max_length=30000) # TODO: can this be markdown style? or at least the stackoverflow style?
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey('MessageBoard', on_delete=models.CASCADE)
    # upvotes = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    # children = models.ManyToMany('Comment', null=True, on_delete=models.SET_NULL, blank=True)
