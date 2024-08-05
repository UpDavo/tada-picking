from django.core.paginator import Paginator
from core.models import Client, ClientOrders, Invoice, PackRule, Stock
from django.utils import timezone
from django.db import IntegrityError, transaction
# from django.urls import reverse_lazy


class ClientService:

    @staticmethod
    def getList(request, name):
        # Obtener todos los usuarios
        items = Client.objects.order_by('created_at').all()

        if name:
            items = items.filter(name__icontains=name)

        # Obtener los campos del modelo Usuario como una lista de objetos Field
        fields = Client._meta.fields
        fields_to_include = ['id', 'created_at', 'name', 'ci', 'email']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los usuarios
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        list_url = 'dashboard:clients'

        # Obtener los valores de los campos para cada usuario
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, list_url

    @staticmethod
    def getOrderList(request, name):
        # Obtener todos los usuarios
        items = ClientOrders.objects.order_by('created_at').all()

        if name:
            items = items.filter(order_number__icontains=name)

        # Obtener los campos del modelo Usuario como una lista de objetos Field
        fields = ClientOrders._meta.fields
        fields_to_include = ['id', 'created_at', 'client',
                             'order_number', 'assigned_code', 'is_confirmed', 'is_email_sended']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los usuarios
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        list_url = 'dashboard:orders'

        # Obtener los valores de los campos para cada usuario
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, list_url

    @staticmethod
    def checkUses(quantity, user_ci):
        # Obtener la fecha actual
        now = timezone.now()

        # Calcular el primer día del mes actual
        first_day_of_month = now.replace(day=1)

        # Filtrar las órdenes del cliente creadas desde el primer día del mes actual
        orders = ClientOrders.objects.filter(
            client__ci=user_ci,
            created_at__gte=first_day_of_month
        )

        # Comparar la cantidad de órdenes con el límite
        if orders.count() >= quantity:
            return False
        else:
            return True

    @staticmethod
    def checkClientExists(user_ci):
        try:
            client = Client.objects.get(ci=user_ci)
            return client
        except Client.DoesNotExist:
            return False

    @staticmethod
    def createClient(ci, name, email):
        try:
            # Crear una nueva instancia de Client
            client = Client(ci=ci, name=name, email=email)
            # Guardar el cliente en la base de datos
            client.save()
            return client
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def createOrder(client_ci, order_number, assigned_code=None, is_email_sended=False):
        try:
            # Obtener el cliente por CI
            client = Client.objects.get(ci=client_ci)

            # Crear una nueva instancia de ClientOrders
            with transaction.atomic():
                order = ClientOrders(
                    client=client,
                    order_number=order_number,
                    assigned_code=assigned_code,
                    is_email_sended=is_email_sended
                )
                # Guardar la orden en la base de datos
                order.save()

            return order
        except Client.DoesNotExist:
            return "Error: Cliente no encontrado."
        except IntegrityError:
            return "Error: Orden con este número ya existe."
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def checkExists(item):
        exists = Client.objects.filter(name=item).exists()
        return exists

    @staticmethod
    def getModel():
        return Client

    @staticmethod
    def getAllItems():
        return Client.objects.all()

    # Transactions

    @staticmethod
    def updateOrderStatus():
        return False

    @staticmethod
    def assignAndValidate(order_id):
        try:
            order = ClientOrders.objects.filter(order_number=order_id).first()

            # Verificar si la orden ya tiene un código asignado
            if order.assigned_code:
                return

            invoice = Invoice.objects.filter(order_id=order_id).first()
            rules = PackRule.objects.all()
            client = order.client

            # Convertir las cantidades de strings a enteros
            bottles = invoice.bottles
            total_bottles = sum(int(quantity) for quantity in bottles.values())

            # Filtrar las reglas generales y ordenarlas por general_quantity
            general_rules = sorted(
                [rule for rule in rules if rule.is_general],
                key=lambda r: r.general_quantity
            )

            # Encontrar la regla que hace match con total_bottles
            selected_rule = None
            previous_quantity = None

            for rule in general_rules:
                if rule.general_quantity == total_bottles:
                    selected_rule = rule
                    break
                elif previous_quantity is not None and previous_quantity <= total_bottles < rule.general_quantity:
                    selected_rule = rule
                    break
                previous_quantity = rule.general_quantity

            if selected_rule:
                # Buscar el código del producto de la regla seleccionada en el stock
                product_stock = Stock.objects.filter(
                    product=selected_rule.product).first()

                if product_stock and product_stock.quantity > 0:
                    # Asignar el código del stock a la orden
                    order.assigned_code = product_stock.code
                    order.is_confirmed = 'confirmed'
                    order.save()

                    # Decrementar la cantidad en el stock
                    product_stock.quantity -= 1
                    if product_stock.quantity == 0:
                        product_stock.delete()
                    else:
                        product_stock.save()

                    # Enviar email si el cliente tiene email
                    if client.email:
                        order.is_email_sended = True
                        order.save()

                        # Placeholder para el envío de email
                        # send_email_to_client(client.email, order)

            else:
                # No se encontró ninguna regla que coincida con la cantidad total de botellas
                return

        except ClientOrders.DoesNotExist:
            # La orden con ID no existe
            return
