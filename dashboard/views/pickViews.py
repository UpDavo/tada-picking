from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from core.models import Bottle, Invoice, Store
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        return context

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        store_id = request.POST.get('store')
        description = request.POST.get('description')
        product_photo = request.FILES.get('product_photo')
        bottles = request.POST.getlist('bottles')

        # Validar que todos los campos estén presentes
        if not order_id or not store_id or not description or not product_photo or not bottles:
            messages.error(request, 'Todos los campos son obligatorios.')
            return self.get(request, *args, **kwargs)

        # Procesar las botellas y cantidades
        bottle_quantities = {bottle.split(':')[0]: bottle.split(':')[1] for bottle in bottles}

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