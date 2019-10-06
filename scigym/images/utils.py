from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage as storage

from scigym.config.models import ImageConfig
from scigym.images.models import Image

import logging
import os
import uuid

logger = logging.getLogger('django')


def save_image(uploaded_file: InMemoryUploadedFile, user) -> Image:
    """process requested file

    Parameters
    ----------
    uploaded_file : InMemoryUploadedFile
        file uploaded by the user
    user : object
        the user who uploaded the image

    Returns
    -------
    Image object
        the new image object that has been created
    """
    # get valid file type
    valid_file_types = ImageConfig.objects.load().valid_image_formats
    valid_file_types_str = ','.join(valid_file_types)
    logger.debug(f'valid file types: {valid_file_types_str}')

    # get file name
    file_name = uploaded_file.name

    # check file extension
    _, file_extension = os.path.splitext(file_name)
    if file_extension.lower() not in valid_file_types:
        raise TypeError('Invalid image format. Valid image formats: {}'.format(valid_file_types_str))

    uuid_name = f'{uuid.uuid4()}{file_extension}'
    with storage.open(uuid_name, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    # save image object
    return Image.objects.create(
        name=file_name,
        file_path=storage.url(uuid_name),
        owner=user,
    )


def delete_image(file_path: str) -> None:
    """removes an uploaded image

    Parameters
    ----------
    file_path - file path of the uploaded file

    """
    logger.info(f'Deleting image with path: {file_path}')

    os.unlink(file_path)
