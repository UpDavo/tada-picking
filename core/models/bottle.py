from django.db import models
from .timeStampedModel import TimeStampedModel


class Bottle(TimeStampedModel):
    type = models.CharField(max_length=255)
    min_bottles = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='bottle_images/', null=True, blank=True)

    def __str__(self):
        return self.type
