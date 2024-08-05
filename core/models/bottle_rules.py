from django.db import models
from .timeStampedModel import TimeStampedModel
from .product import Product
from .bottle import Bottle


class PackRule(TimeStampedModel):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bottles = models.ManyToManyField(Bottle, through='BottleQuantity')
    # Nuevo campo para indicar si es una regla general
    is_general = models.BooleanField(default=False)
    general_quantity = models.IntegerField(
        default=0, blank=True, null=True)  # Cantidad para reglas generales

    def __str__(self):
        return f"PackRule for {self.product.name} - {self.name}"


class BottleQuantity(models.Model):
    pack_rule = models.ForeignKey(PackRule, on_delete=models.CASCADE)
    bottle = models.ForeignKey(Bottle, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.bottle.type} in {self.pack_rule.name}"
