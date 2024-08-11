from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from core.models import Bottle, Invoice, Client, ClientOrders, Store
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.services.client_service import ClientService
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

PERMISSION = 'dashboard:picking'


class PickingForm(TemplateView):
    template_name = 'pages/picking/form_picking_page.html'

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
        user_phone = request.POST.get('user_phone')
        quantity_limit = 3

        # Verificar límite de pedidos
        if not ClientService.checkUses(quantity_limit, user_phone):
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

        # try:
        # Crear la factura
        invoice = Invoice.objects.create(
            store_id=store_id,
            picker=picker,
            client=Client.objects.filter(phone_number=user_phone).first(),
            description=description,
            product_photo=product_photo,
            bottles=bottle_quantities
        )

        # Crear la orden
        ClientService.createOrder(
            user_phone, invoice.order_id)
        messages.success(request, 'Orden creada exitosamente.')
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

        numero_celular = data.get('numero', None)

        if numero_celular:
            # print(f"Número de celular recibido: {numero_celular}")
            client = Client.objects.filter(phone_number=numero_celular).first()

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
