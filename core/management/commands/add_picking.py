from django.core.management.base import BaseCommand
from core.models import Client

class Command(BaseCommand):
    help = 'Add all URLs from urlpatterns as permissions'

    def handle(self, *args, **options):
        
        invoices = Client.objects.all()
        
        for invoice in invoices:
            invoice.delete()
