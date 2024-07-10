from django.core.management.base import BaseCommand
from core.models import Invoice, Store, Bottle

class Command(BaseCommand):
    help = 'Add all URLs from urlpatterns as permissions'

    def handle(self, *args, **options):
        
        store = Store.objects.first()

        Invoice.objects.create(
            order_id="OR120033",
            store=store,
            picker_name="John Doe",
            picker_ci=123456789,
            description="Descripción de la factura",
            bottles={
                1: 5,
               2: 5,
                3: 5
            }
        )
