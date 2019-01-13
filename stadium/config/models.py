import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField

from stadium.users.models import User


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug
