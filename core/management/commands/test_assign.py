from django.core.management.base import BaseCommand
from core.utils.emailThread import EmailThread
from core.models import ClientOrders, Invoice, PackRule, Stock, Bottle, BottleQuantity
import pandas as pd


class Command(BaseCommand):
    help = 'Send a custom test email using EmailThread'

    def handle(self, *args, **kwargs):
        order_id = 'INV-20240905-0001'

        order = ClientOrders.objects.filter(order_number=order_id).first()

        # Verificar si la orden ya tiene un código asignado
        if order.assigned_code:
            return

        invoice = Invoice.objects.filter(order_id=order_id).first()
        client = order.client

        # Botellas del pedido
        bottles = invoice.bottles

        # Crear una lista para almacenar las botellas y sus cantidades
        bottles_with_quantities = []

        # Recorrer el diccionario de botellas del pedido y buscar las botellas por su ID
        for bottle_id, quantity in bottles.items():
            try:
                # Buscar la instancia de Bottle por su ID y convertir la cantidad a entero
                bottle = Bottle.objects.get(id=bottle_id)
                quantity = int(quantity)
                bottles_with_quantities.append(
                    {'bottle': bottle, 'quantity': quantity})
            except Bottle.DoesNotExist:
                print(f'Bottle with ID {bottle_id} does not exist')

        # Reglas (PackRules)
        rules = PackRule.objects.all()

        # Variable para almacenar la primera regla coincidente
        selected_rule = None

        # Recorrer todas las PackRules y detenerse cuando se encuentre la primera coincidencia
        for rule in rules:
            rule_bottles = BottleQuantity.objects.filter(pack_rule=rule)

            match = True
            for order_bottle in bottles_with_quantities:
                # Verificar si la botella del pedido coincide con la botella de la regla
                matching_bottle = rule_bottles.filter(
                    bottle=order_bottle['bottle']).first()
                if not matching_bottle or matching_bottle.quantity != order_bottle['quantity']:
                    match = False
                    break

            if match:
                selected_rule = rule
                break

        # Si se encuentra una regla coincidente, procesar el stock y enviar el email
        if selected_rule:
            print(
                f'Regla coincidente para el pedido {order_id}: {selected_rule.name} (Producto: {selected_rule.product.name})')

            product_stock = Stock.objects.filter(
                product=selected_rule.product).first()

            if product_stock and product_stock.quantity > 0:
                # Asignar el código del stock a la orden
                print(product_stock.code)
                order.assigned_code = product_stock.code
                order.is_confirmed = 'confirmed'

                # Decrementar la cantidad en el stock
                product_stock.quantity -= 1
                if product_stock.quantity == 0:
                    product_stock.delete()
                else:
                    product_stock.save()

                # Enviar email si el cliente tiene email
                if client.email:
                    subject = 'Su picking de botella le ha dado un cupón'
                    email_data = {'code': product_stock.code}
                    recipient_list = [client.email]
                    template = 'emails/assigned_code.html'

                    email_thread = EmailThread(
                        subject, email_data, recipient_list, template)

                    try:
                        email_thread.start()
                        order.is_email_sended = True
                    except Exception as e:
                        order.is_email_sended = False
                        print("Exception while sending email:", e)

                order.save()
        else:
            print(f'No hay reglas coincidentes para el pedido {order_id}.')
