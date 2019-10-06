import logging

from django.db.models.signals import pre_delete 
from django.dispatch import receiver

from scigym.images.models import Image
from scigym.images.utils import delete_image

logger = logging.getLogger('django')


@receiver(pre_delete, sender=Image)
def delete_file(sender, instance: Image, **kwargs):
    if sender == Image:
        logger.info('Deleting image: {}'.format(instance.file_path))
        delete_image(instance.name)
