from django.db import models
from django.db.models import JSONField
from .timeStampedModel import TimeStampedModel
from .store import Store
from .client import Client  # Importar el modelo Client
from .user import User
from core.utils.storage_backend import PublicUploadStorage
import datetime


class Invoice(TimeStampedModel):
    STATUS_CHOICES = [
        ('awaiting_approval', 'Esperando Aprobación'),
        ('approved', 'Aprobado'),
        ('approved_but_incomplete', 'Aprobado con Detalle'),
    ]

    order_id = models.CharField(max_length=20, unique=True, editable=True)

    # Recogedor (picker), con opción de que quede nulo si el usuario es eliminado
    picker = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    # Nombre del picker (almacenado como histórico)
    picker_name = models.CharField(max_length=255, blank=True, null=True)

    # Cliente (permite null cuando el cliente es eliminado)
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True)

    # Nombre del cliente (almacenado como histórico)
    client_name = models.CharField(max_length=255, blank=True, null=True)

    # Tienda (permite null cuando la tienda es eliminada)
    store = models.ForeignKey(
        Store, on_delete=models.SET_NULL, null=True, blank=True)

    # Nombre de la tienda (almacenado como histórico)
    store_name = models.CharField(max_length=255, blank=True, null=True)

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

    def save(self, *args, **kwargs):
        # Si el picker está presente, guarda su nombre como histórico
        if self.picker:
            # Almacenar el nombre del picker como histórico
            self.picker_name = self.picker.names

        # Si la tienda está presente, guarda su nombre como histórico
        if self.store:
            # Almacenar el nombre de la tienda como histórico
            self.store_name = self.store.name

        # Si el cliente está presente, guarda su nombre como histórico
        if self.client:
            # Almacenar el nombre del cliente (puedes cambiar a nombre)
            self.client_name = self.client.ci

        if not self.order_id:
            today = datetime.date.today().strftime("%Y%m%d")
            last_invoice = Invoice.objects.filter(
                order_id__icontains=today).order_by('order_id').last()
            if last_invoice:
                last_id = int(last_invoice.order_id[-4:])
                new_id = f"{today}-{str(last_id + 1).zfill(4)}"
            else:
                new_id = f"{today}-0001"
            self.order_id = f"INV-{new_id}"

        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.order_id} for {self.client_name or 'N/A'} at {self.store_name or 'N/A'}"

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
