from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

from scigym.config.models import ImageConfig
from scigym.images.models import Image

import logging
from typing import List, Tuple
import uuid
from uuid import UUID
import os
import pathlib
import zipfile
import tarfile
import hashlib
from shutil import copyfile, rmtree

logger = logging.getLogger('django')

SAVED_IMAGES = settings.SAVED_IMAGES
TEMP_IMAGES = settings.TEMP_IMAGES

def save_image(uploaded_file: InMemoryUploadedFile, description: str) -> List[Image]:
    """ process all requested files

    Parameters
    ----------
    uploaded_file : InMemoryUploadedFile
        file uploaded by the user
    description : str
        description for the image

    Returns
    -------
    list of Image objects
        list of all new Image objects that were created
    """
    #get valid image type
    valid_file_types = ImageConfig.objects.load().valid_image_formats
    valid_file_types_str = ','.join(valid_file_types)
    logger.debug(f'valid file types: {valid_file_types_str}')

    #create a unique temporary directory and save files to it
    unique_dir = uuid.uuid4()  # scope all operations to a directory for this request
    temp_file_path = save_to_temp(unique_dir, uploaded_file)
    logger.info(f'Beginning file processing for: {temp_file_path}')
    logger.info(f'Checking for file extensions using: {valid_file_types_str}')

    #process files in temp directory and save to permanent one
    saved_files = []
    new_files = 0
    #get valid and unique files
    for file_name, file_path in process_files(valid_file_types, temp_file_path):
        #hash file
        hash_string = hash_file(file_path)
        #create new file object
        try:
            saved_image = Image.objects.get(hash=hash_string)
            logger.debug(f'Image already exists: {file_name}')
        except Image.DoesNotExist:
            saved_image = save_image_object(file_name, file_path, hash_string, description)
            new_files += 1
        saved_files.append(saved_image)

    #remove temp directory
    clean_temp_directory(temp_file_path)
    logger.info(f'Finished processing files. Total: {len(saved_files)} New: {new_files}')
    return saved_files

def save_to_temp(unique_dir: UUID, file: InMemoryUploadedFile) -> str:
    """ Save the file to temporary storage
    Parameters
    ----------
    unique_dir: UUID
        unique directory that this operation is scoped to
    file : django.core.files.uploadedfile.InMemoryUploadedFile
        File uploaded by the user

    Returns
    -------
    file_path : str
        file path of the saved file
    """
    file_directory = f'{TEMP_IMAGES}/{unique_dir}'
    file_path = f'{file_directory}/{file.name}'
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)
    logger.info(os.path.exists(TEMP_IMAGES))
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

def process_files(valid_file_types: List[str], temp_file_path: str) -> List[Tuple[str, str]]:
    """Checks that file in the temp directory is a valid file
    Returns
    -------
    list of str
        list of files with an image extension
    """
    processed_files = []
    logger.info(f'Processing files in {os.path.dirname(temp_file_path)}')
    for root, dirs, files in os.walk(os.path.dirname(temp_file_path)):
        for file in files:
            if is_valid_file(valid_file_types, os.path.join(root, file)):
                processed_files.append((file, os.path.join(root, file)))
    logger.info(f'Processed files: {processed_files}')
    return processed_files

def is_valid_file(valid_file_types: List[str], file_path: str) -> bool:
    """

    Parameters
    ----------
    file_path : str
        path to the file we are checking

    Returns
    -------
    bool
        if the file name has an software extension
    """
    file_type = ''.join(pathlib.Path(file_path).suffixes)
    valid_file = file_type in valid_file_types
    if not valid_file:
        logger.warning(f'Ignoring for incorrect file type: {file_type} - {file_path} among {valid_file_types}')
    return valid_file

def hash_file(file_path: str) -> str:
    """Generate a hash for the file located at this file path

    Parameters
    ----------
    file_path : str
        file path to hash

    Returns
    -------
    str
        md5 hash of the file

    """
    md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            md5.update(chunk)
        hash_string = md5.hexdigest()
        logger.debug(f'Created hash {hash_string} for file: {file_path}')
        return hash_string

def save_image_object(file_name: str, file_path: str, hash_string: str, description: str) -> Image:
    """saves an image into the database

    Parameters
    ----------
    file_name : str
        original name of the file
    file_path : str
        full file path
    hash_string: str
        md5 hash of the file
    description: str
        description of the image object

    Returns
    -------
    Image
        Image object created in the database

    """
    _, file_extension = os.path.splitext(file_name)
    uuid_name = f'{uuid.uuid4()}{file_extension}'
    save_path = os.path.join(SAVED_IMAGES, uuid_name)
    copyfile(file_path, save_path)
    return Image.objects.create(
        name=file_name,
        file_path=save_path,
        hash=hash_string,
        description=description,
    )

def clean_temp_directory(temp_file_path: str) -> None:
    """remove all files & directories from the temp directory

    Parameters
    ----------
    temp_file_path - file path of the original file uploaded by the user

    """
    logger.debug(f'Clearing temporary file path: {os.path.dirname(temp_file_path)}')

    rmtree(os.path.dirname(temp_file_path))

def delete_image(file_path: str) -> None:
    """removes an uploaded image

    Parameters
    ----------
    file_path - file path of the uploaded file

    """
    logger.info(f'Deleting image with path: {file_path}')

    os.unlink(file_path)
