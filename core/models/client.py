from django.db import models
from .timeStampedModel import TimeStampedModel


class Client(TimeStampedModel):
    ci = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.ci
