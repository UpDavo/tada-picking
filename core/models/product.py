from django.db import models
from .timeStampedModel import TimeStampedModel
from core.utils.storage_backend import PublicUploadStorage


class Product(TimeStampedModel):
    name = models.CharField(max_length=45)
    sku = models.IntegerField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    active = models.BooleanField(default=True)
    starred = models.BooleanField(default=False)
    is_fisical = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/',
                              storage=PublicUploadStorage(), null=True, blank=True, default='')

    def __str__(self):
        return self.name
