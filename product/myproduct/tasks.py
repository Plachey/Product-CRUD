import logging
import time
from io import BytesIO

from PIL import Image
from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404
from product.celery import app

from .models import Products

logger = logging.getLogger(__name__)


@app.task()
def async_save(imagefield_data, instance):
    file_info = list()

    file_info.append(imagefield_data.field_name)
    file_info.append(imagefield_data.name)
    file_info.append(imagefield_data.content_type)
    file_info.append(imagefield_data.size)
    file_info.append(imagefield_data.charset)

    instance = get_object_or_404(Products, uuid=instance['uuid'])
    logger.info('Task instance: {}'.format(instance))

    im = Image.open(imagefield_data)
    start = time.time()
    logger.info('Task start rotate: {}'.format(start))
    # rotate image
    tmp = im.rotate(180)
    # got result rotate
    result = time.time() - start
    logger.info('Task result rotate: {}'.format(result))
    # BytesIO buffer
    img = BytesIO()
    # get format image and save
    tmp.save(img, format=file_info[2].split('/')[1])
    # pass the BytesIo, and a list of required args to InMemoryUploadedFile
    image = InMemoryUploadedFile(img, *file_info)
    # add the name of the formfield to the instance's __dict__, and set the image to it.
    instance.__dict__[file_info[0]] = image
    instance.rotate_duration = result
    logger.info('Task save fielt image, rotate_duration')

    instance.save()
    # invalidate the cache, this is necessary if you are using Johnny Cache,
    # as adding the image to the instance will not invalidate the cache
    cache.clear()
