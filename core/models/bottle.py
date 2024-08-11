from django.db import models
from .timeStampedModel import TimeStampedModel
from core.utils.storage_backend import PublicUploadStorage


class Bottle(TimeStampedModel):
    type = models.CharField(max_length=255)
    min_bottles = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='bottle_images/', storage=PublicUploadStorage(), null=True, blank=True, default='')

    def __str__(self):
        return self.type
