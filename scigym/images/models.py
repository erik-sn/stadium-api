from django.db import models

from scigym.config.models import Base
from scigym.users.models import User


class Image(Base):
    name = models.CharField(max_length=255)
    file_path = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
