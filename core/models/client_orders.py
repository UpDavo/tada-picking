from django.db import models
from .timeStampedModel import TimeStampedModel
from .client import Client


class ClientOrders(TimeStampedModel):
    PENDING_CONFIRM = 'pending_confirm'
    CONFIRMED = 'confirmed'

    CONFIRMATION_STATUS_CHOICES = [
        (PENDING_CONFIRM, 'Pending Confirmation'),
        (CONFIRMED, 'Confirmed'),
    ]

    # Cliente (se establece en null cuando el cliente es eliminado)
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True)

    # Nombre del cliente (almacenado como histórico)
    client_email = models.CharField(max_length=255, null=True, blank=True)

    order_number = models.CharField(max_length=255, null=False, blank=False)
    assigned_code = models.CharField(max_length=255, null=True, blank=True)
    is_confirmed = models.CharField(
        max_length=20,
        choices=CONFIRMATION_STATUS_CHOICES,
        default=PENDING_CONFIRM,
    )
    is_email_sended = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si el cliente está presente, guarda su nombre como histórico
        if self.client:
            # Almacenar el nombre del cliente como histórico
            self.client_email = self.client.email

        super(ClientOrders, self).save(*args, **kwargs)

    def __str__(self):
        order_number_str = self.order_number or "No Order Number"
        client_email_str = self.client_email or "No Client"
        return f"Order {order_number_str} for {client_email_str}"
