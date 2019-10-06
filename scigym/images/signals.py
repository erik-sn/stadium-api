import logging
import os

from django.db.models.signals import pre_delete 
from django.dispatch import receiver

from scigym.images.models import Image
from scigym.images.utils import delete_image

logger = logging.getLogger('django')


@receiver(pre_delete, sender=Image)
def delete_file(sender, instance, **kwargs):
    if sender == Image:
        delete_image(instance.file_path)
