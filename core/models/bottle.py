from django.db import models
from .timeStampedModel import TimeStampedModel
import uuid

class Bottle(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type