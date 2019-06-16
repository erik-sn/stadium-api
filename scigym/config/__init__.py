from .local import Local  # noqa
from .production import Production  # noqa
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # Build file directory if not already in existence
SAVED_IMAGES = os.path.join(BASE_DIR, 'files', 'images')
if not os.path.exists(SAVED_IMAGES):
    os.makedirs(SAVED_IMAGES)
