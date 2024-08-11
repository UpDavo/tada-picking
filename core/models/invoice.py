import uuid
from django.db import models
from django.db.models import JSONField
from .timeStampedModel import TimeStampedModel
from .store import Store
from .client import Client  # Importar el modelo Client
from .user import User
from core.utils.storage_backend import PublicUploadStorage


class Invoice(TimeStampedModel):
    STATUS_CHOICES = [
        ('awaiting_approval', 'Esperando Aprobación'),
        ('approved', 'Aprobado'),
        ('approved_but_incomplete', 'Aprobado con Detalle'),
    ]

    # ID de Invoice único
    # order_id = models.CharField(max_length=30, unique=True)

    order_id = models.UUIDField(
        default=uuid.uuid4,
        editable=True,
        unique=True,
    )

    # Recogedor
    picker = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1)

    # Cliente
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, default=2)

    # Tienda
    # default ID para tienda
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1)

    # Detalles
    description = models.CharField(max_length=150, default='Ninguno')

    # Botellas
    bottles = JSONField(default=dict)

    # Foto del Producto
    product_photo = models.ImageField(
        upload_to='invoice_photos/', storage=PublicUploadStorage(), null=True, blank=True, default='default.jpg')

    # Detalles de Aprobación
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='awaiting_approval')
    approval_comment = models.TextField(blank=True, null=True)
    updated_bottles = JSONField(blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.invoice_id} for {self.client.ci} at {self.store.name}"

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
