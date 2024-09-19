from django.core.paginator import Paginator
from core.models import ClientOrders, Invoice, PackRule, Stock, Bottle, BottleQuantity, Client
from django.utils import timezone
from django.db import IntegrityError, transaction
from openpyxl import Workbook
from django.http import HttpResponse
from core.utils.emailThread import EmailThread
import pytz
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
        fields_to_include = ['id', 'created_at',
                             'ci', 'name', 'email']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los usuarios
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        list_url = 'dashboard:clients'
        upload_url = 'dashboard:clients_upload_general'

        # Obtener los valores de los campos para cada usuario
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, list_url, upload_url

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
    def checkUses(quantity, user_email):
        # Obtener la fecha actual
        now = timezone.now()

        # Calcular el primer día del mes actual
        first_day_of_month = now.replace(day=1)

        # Filtrar las órdenes del cliente creadas desde el primer día del mes actual
        orders = ClientOrders.objects.filter(
            client__email=user_email,
            created_at__gte=first_day_of_month
        )

        # Comparar la cantidad de órdenes con el límite
        if orders.count() >= quantity:
            return False
        else:
            return True

    @staticmethod
    def checkClientExists(user_phone):
        try:
            client = Client.objects.get(phone_number=user_phone)
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
    def createOrder(user_email, order_number, assigned_code=None, is_email_sended=False):
        try:
            # Obtener el cliente por CI
            client = Client.objects.get(email=user_email)

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
            ecuador_tz = pytz.timezone('America/Guayaquil')

            # Obtener la fecha y hora actual en la zona horaria de Ecuador
            current_datetime = timezone.now().astimezone(ecuador_tz)

            # Formatear la fecha y la hora
            months = {
                1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
                7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
            }

            # Formatear la fecha en el formato deseado
            formatted_date = f"{current_datetime.day} de {months[current_datetime.month]} del {current_datetime.year} a las {current_datetime.strftime('%H:%M')}"

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

            bottles_array = [
                f"{bottle['quantity']} - {bottle['bottle']}" for bottle in bottles_with_quantities]

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
                        email_data = {
                            'nombre': client.name,
                            'order_id': invoice.order_id,
                            'code':  product_stock.code,
                            'value': selected_rule.product.name,
                            'picker_name': invoice.picker.names,
                            'pick_date': formatted_date,
                            'bottles': bottles_array
                        }
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

        except ClientOrders.DoesNotExist:
            # La orden con ID no existe
            return

    @staticmethod
    def create_excel_template2():
        # Crear un libro de trabajo
        wb = Workbook()
        ws = wb.active

        # Definir los títulos de las columnas
        columns = ['ci', 'nombre', 'email']
        ws.append(columns)

        # Guardar el libro en un objeto de respuesta HTTP
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Plantilla_codigos_skus.xlsx"'
        wb.save(response)

        return response

    @staticmethod
    def uploadDataframe(df):
        # Renombrar columnas para que coincidan con los campos del modelo Client
        df.rename(columns={
            'nombre': 'name',
            'ci': 'ci',
            'email': 'email'
        }, inplace=True)

        # Convertir todas las columnas del DataFrame a tipo string
        df = df.astype(str)

        # Filtrar los emails que no son None o vacíos
        df = df[df['email'].notna() & df['email'].str.strip().ne('')]

        # Obtener todos los CIs de los clientes existentes y convertirlos a strings
        existing_cis = set(str(ci)
                           for ci in Client.objects.values_list('ci', flat=True))

        # Obtener todos los emails de los clientes existentes y convertirlos a strings
        existing_emails = set(
            str(email) for email in Client.objects.values_list('email', flat=True))

        # Filtrar el DataFrame para eliminar filas con CIs existentes
        df_filtered = df[~df['ci'].isin(existing_cis)]

        # Filtrar el DataFrame para eliminar filas con emails existentes
        df_filtered = df_filtered[~df_filtered['email'].isin(existing_emails)]

        # Crear una lista de instancias de clientes que necesitan ser creadas
        clients_to_create = [
            Client(
                ci=row['ci'],
                name=row['name'],
                email=row['email']
            )
            # Solo iteramos sobre los registros filtrados
            for _, row in df_filtered.iterrows()
        ]

        # Insertar todos los nuevos clientes en la base de datos en un solo paso
        if clients_to_create:
            Client.objects.bulk_create(clients_to_create)
