from django.db import models
from .timeStampedModel import TimeStampedModel
from core.utils.storage_backend import PublicUploadStorage


class Bottle(TimeStampedModel):
    type = models.CharField(max_length=255)
    min_bottles = models.IntegerField(default=3, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    bottle_range = models.IntegerField(default=3, blank=False, null=False)
    image = models.ImageField(
        upload_to='bottle_images/', storage=PublicUploadStorage(), null=True, blank=True, default='')

    def __str__(self):
        return self.type
