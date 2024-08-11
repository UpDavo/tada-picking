from django.core.management.base import BaseCommand
from core.models import Client


class Command(BaseCommand):
    help = 'Create new clients'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clients',
            nargs='+',
            type=str,
            help='List of clients to create, formatted as ci:name:email:phone_number',
        )

    def handle(self, *args, **options):
        clients_data = options['clients']

        if clients_data:
            for client_str in clients_data:
                ci, name, email, phone_number = client_str.split(':')
                client, created = Client.objects.get_or_create(
                    ci=ci,
                    defaults={
                        'name': name,
                        'email': email,
                        'phone_number': phone_number
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully created client with CI {ci}'))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Client with CI {ci} already exists'))
        else:
            self.stdout.write(self.style.ERROR('No client data provided'))
