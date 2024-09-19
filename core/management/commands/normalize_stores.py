import re
from django.core.management.base import BaseCommand
from core.models import User, Store


def normalize_store_name(store_name):
    # Convierte el nombre a minúsculas y elimina caracteres especiales
    return re.sub(r'[^a-z0-9]+', '', store_name.lower())


class Command(BaseCommand):
    help = 'Normaliza nombres de tiendas y elimina duplicados si es necesario'

    def handle(self, *args, **kwargs):
        stores_normalized = {}
        users = User.objects.select_related('store').all()

        for user in users:
            normalized_name = normalize_store_name(user.store.name)

            if normalized_name in stores_normalized:
                # Si la tienda ya existe normalizada pero es diferente, reasigna el usuario a la tienda existente
                existing_store = stores_normalized[normalized_name]
                if existing_store != user.store.id:
                    # Reasigna al usuario a la tienda ya existente
                    user.store = Store.objects.get(id=existing_store)
                    user.save()
                    self.stdout.write(self.style.WARNING(
                        f'El usuario {user.username} ha sido reasignado a la tienda {user.store.name}.'))
            else:
                # Guarda la tienda normalizada y actualiza su nombre
                user.store.name = normalized_name
                user.store.save()
                stores_normalized[normalized_name] = user.store.id
                self.stdout.write(self.style.SUCCESS(
                    f'Tienda actualizada: {user.store.name}'))

        self.stdout.write(self.style.SUCCESS(
            'Normalización y eliminación de duplicados completada.'))
