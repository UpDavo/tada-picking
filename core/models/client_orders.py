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

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, null=False, blank=False)
    assigned_code = models.CharField(max_length=255, null=True, blank=True)
    is_confirmed = models.CharField(
        max_length=20,
        choices=CONFIRMATION_STATUS_CHOICES,
        default=PENDING_CONFIRM,
    )
    is_email_sended = models.BooleanField(default=False)

    def __str__(self):
        order_number_str = self.order_number or "No Order Number"
        client_name_str = self.client.name if self.client else "No Client"
        return f"Order {order_number_str} for {client_name_str}"
