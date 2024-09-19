from django.views.generic import TemplateView
from django.shortcuts import redirect
from core.models import Bottle, Invoice, Client, Store
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.services.client_service import ClientService
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.utils.emailThread import EmailThread
from django.utils import timezone
import pytz

PERMISSION = 'dashboard:picking'


class PickingForm(TemplateView):
    template_name = 'pages/picking/form_picking_page_bundle.html'

    def dispatch(self, request, *args, **kwargs):
        if settings.LOCAL:
            return super().dispatch(request, *args, **kwargs)
        else:
            user = request.user
            if not user.is_authenticated:
                return login_required(login_url=reverse_lazy(settings.LOGIN))(super().dispatch)(request, *args, **kwargs)
            if user.has_permission(PERMISSION):
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect(settings.NOT_ALLOWED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'Crear Picking'
        context['botellas'] = Bottle.objects.all()
        context['stores'] = Store.objects.filter(name=self.request.user.store)
        # Fix
        context['max_bottles'] = 24
        return context

    def post(self, request, *args, **kwargs):
        picker = request.user
        store_id = request.POST.get('store')
        description = request.POST.get('description')
        product_photo = request.FILES.get('product_photo')
        bottles = request.POST.getlist('bottles')
        user_email = request.POST.get('user_email')
        quantity_limit = 3

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

        # Verificar límite de pedidos
        if not ClientService.checkUses(quantity_limit, user_email):
            messages.error(
                request, f'El cliente ya hizo el límite de {quantity_limit} pedidos al mes')
            return self.get(request, *args, **kwargs)

        # print(store_id, description, product_photo, bottles, user_phone, picker)

        # Validar que todos los campos estén presentes
        if not store_id or not description or not product_photo or not bottles:
            messages.error(request, 'Todos los campos son obligatorios.')
            return self.get(request, *args, **kwargs)

        # Procesar las botellas y cantidades
        bottle_quantities = {bottle.split(':')[0]: bottle.split(':')[
            1] for bottle in bottles}

        client = Client.objects.filter(email=user_email).first()

        # Crear la factura
        invoice = Invoice.objects.create(
            store_id=store_id,
            picker=picker,
            client=client,
            description=description,
            product_photo=product_photo,
            bottles=bottle_quantities
        )

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

        # Crear la orden
        ClientService.createOrder(
            user_email, invoice.order_id)

        messages.success(request, 'Orden creada exitosamente.')

        subject = 'Su órden de picking ha sido creada exitosamente'
        email_data = {
            'nombre': client.name,
            'order_id': invoice.order_id,
            'code': '',
            'value': 0,
            'picker_name': picker.names,
            'pick_date': formatted_date,
            'bottles': bottles_array
        }
        recipient_list = [client.email]
        template = 'emails/picking_complete.html'

        email_thread = EmailThread(
            subject, email_data, recipient_list, template)

        try:
            email_thread.start()
        except Exception as e:
            print("exception", e)

        # except IntegrityError:
        #     messages.error(
        #         request, f'Error al crear la factura.')
        #     return self.get(request, *args, **kwargs)

        return redirect('dashboard:picking_complete')


class PickingComplete(TemplateView):
    template_name = 'pages/picking/complete_view.html'

    def dispatch(self, request, *args, **kwargs):
        if settings.LOCAL:
            return super().dispatch(request, *args, **kwargs)
        else:
            user = request.user
            if not user.is_authenticated:
                return login_required(login_url=reverse_lazy(settings.LOGIN))(super().dispatch)(request, *args, **kwargs)
            if user.has_permission(PERMISSION):
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect(settings.NOT_ALLOWED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = 'Crear Picking'


@csrf_exempt
def verificar_celular(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'verificado': False, 'mensaje': 'Formato de datos no válido'}, status=400)

        correo = data.get('correo', None)

        if correo:
            # print(f"Número de celular recibido: {numero_celular}")
            client = Client.objects.filter(email=correo).first()

            if client:
                # El número está registrado
                return JsonResponse({'verificado': True, 'mensaje': 'Número verificado correctamente'})
            else:
                # El número no está registrado
                return JsonResponse({'verificado': False, 'mensaje': 'Número no registrado'}, status=404)
        else:
            return JsonResponse({'verificado': False, 'mensaje': 'Número no proporcionado'}, status=400)
    else:
        return JsonResponse({'verificado': False, 'mensaje': 'Método no permitido'}, status=405)
