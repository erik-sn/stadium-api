from django.db import models

from scigym.config.models import Base
from scigym.users.models import User

class MessageBoard(Base):
    # Message Board style with stackoverflow in mind.
    # Each environment has many Commentary Boards where people can ask questions or comment on the environment.
    # Environments will receive board key.
    title = models.CharField(max_length=150, unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    admin = models.ManyToMany(User, on_delete=models.SET_NULL) # TODO: this is the environment owner # is this redundant?
    comment = models.TextField(max_length=30000) # TODO: can this be markdown style? or at least the stackoverflow style?
    # num_comments = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    upvotes = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    tag = models.ManyToMany('Tag', blank=True)

class Comment(Base):
    comment = models.TextField(max_length=30000) # TODO: can this be markdown style? or at least the stackoverflow style?
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    board = models.ForeignKey('MessageBoard', on_delete=models.CASCADE)
    upvotes = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    children = models.ManyToMany('Comment', null=True, on_delete=models.SET_NULL, blank=True)

class Tag(Base):
    name = models.CharField(max_length=60, unique=True, blank=False)
