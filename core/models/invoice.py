from django.db import models
from django.db.models import JSONField
from .timeStampedModel import TimeStampedModel
from .store import Store

class Invoice(TimeStampedModel):
    STATUS_CHOICES = [
        ('awaiting_approval', 'Esperando Aprobación'),
        ('approved', 'Aprobado'),
        ('approved_but_incomplete', 'Aprobado con Detalle'),
    ]

    order_id = models.CharField(max_length=30, unique=True)
    
    # Tienda
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=0)
    
    # Recogedor
    picker_name = models.CharField(max_length=100, default='John Doe')
    picker_ci = models.IntegerField(default=0)
    
    # Detalles
    description = models.CharField(max_length=150, default='Ninguno')
    
    # Botellas
    bottles = JSONField(default=dict)
    
    # Foto del Producto
    product_photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)
    
    # Detalles de Aprobación
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='awaiting_approval')
    approval_comment = models.TextField(blank=True, null=True)
    updated_bottles = JSONField(blank=True, null=True)

    def __str__(self):
        return self.order_id

    def approve(self):
        self.status = 'approved'
        self.save()

    def approve_but_incomplete(self, comment, updated_bottles):
        self.status = 'approved_but_incomplete'
        self.approval_comment = comment
        self.updated_bottles = updated_bottles
        self.save()

    def set_awaiting_approval(self):
        self.status = 'awaiting_approval'
        self.save()
