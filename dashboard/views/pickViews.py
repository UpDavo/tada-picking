from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from core.models import Bottle, Invoice, Client, ClientOrders, Store
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.services.client_service import ClientService
from django.db.utils import IntegrityError

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
        context['order_id'] = ''
        context['nombre'] = 'Crear Picking'
        context['picker_name'] = self.request.user.get_full_name()
        context['picker_ci'] = self.request.user.ci
        context['botellas'] = Bottle.objects.all()
        context['stores'] = Store.objects.filter(name=self.request.user.store)
        # Fix
        context['max_bottles'] = 24
        return context

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        store_id = request.POST.get('store')
        description = request.POST.get('description')
        product_photo = request.FILES.get('product_photo')
        bottles = request.POST.getlist('bottles')
        user_ci = request.POST.get('user_ci')
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        quantity_limit = 3

        # Verificar límite de pedidos
        if not ClientService.checkUses(quantity_limit, user_ci):
            messages.error(
                request, f'El cliente ya hizo el límite de {quantity_limit} pedidos al mes')
            return self.get(request, *args, **kwargs)

        # Validar que todos los campos estén presentes
        if not order_id or not store_id or not description or not product_photo or not bottles:
            messages.error(request, 'Todos los campos son obligatorios.')
            return self.get(request, *args, **kwargs)

        # Procesar las botellas y cantidades
        bottle_quantities = {bottle.split(':')[0]: bottle.split(':')[
            1] for bottle in bottles}

        # Verificar si el cliente existe
        if not ClientService.checkClientExists(user_ci):
            # Crear cliente si no existe
            client_creation_result = ClientService.createClient(
                user_ci, user_name, user_email)
            if not isinstance(client_creation_result, Client):
                messages.error(
                    request, f'Error al crear el cliente: {client_creation_result}')
                return self.get(request, *args, **kwargs)

        # Crear la orden
        order_creation_result = ClientService.createOrder(user_ci, order_id)
        if not isinstance(order_creation_result, ClientOrders):
            messages.error(
                request, f'Error al crear la orden: {order_creation_result}')
            return self.get(request, *args, **kwargs)

        # Verificar si la factura ya existe
        existing_invoice = Invoice.objects.filter(order_id=order_id).first()
        if existing_invoice:
            messages.error(
                request, f'Ya existe una factura con el número de orden {order_id}.')
            return self.get(request, *args, **kwargs)

        try:
            # Crear la factura
            Invoice.objects.create(
                order_id=order_id,
                store_id=store_id,
                picker_name=request.user.get_full_name(),
                picker_ci=request.user.ci,
                description=description,
                product_photo=product_photo,
                bottles=bottle_quantities
            )
            messages.success(request, 'Orden creada exitosamente.')
        except IntegrityError:
            messages.error(
                request, f'Error al crear la factura. El número de orden {order_id} ya existe.')
            return self.get(request, *args, **kwargs)

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
