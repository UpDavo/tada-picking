from django.db import models
from .timeStampedModel import TimeStampedModel
from .city import City

class Store(TimeStampedModel):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
