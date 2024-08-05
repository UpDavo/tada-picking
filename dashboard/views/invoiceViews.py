from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, View
from django.shortcuts import HttpResponseRedirect
from core.services.invoice_service import InvoiceService
from django.conf import settings
from dashboard.forms import CreateInvoiceForm, ViewInvoiceForm
import json
from django.http import HttpResponse
import pandas as pd
import io
from django.utils.decorators import method_decorator

from core.services.client_service import ClientService

PERMISSION = 'dashboard:invoices'


class InvoiceList(TemplateView):
    template_name = 'pages/generic/generic_table_page.html'

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
                return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get('names')

        page_obj, fields, object_data, list_url, description_url, view_url = InvoiceService.getInvoiceList(
            self.request, name)

        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Picking"
        context['busqueda'] = "número de orden"
        context['key'] = "downloadTable"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['description_url'] = description_url
        context['view_url'] = view_url
        context['list_url'] = list_url

        return context


@method_decorator(login_required, name='dispatch')
class DownloadExcel(View):

    def get(self, request, *args, **kwargs):
        df = InvoiceService.get_excel_data(
            self.request, order_id=request.GET.get('names'))

        # Crear un archivo Excel en memoria
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        # Obtener el contenido del archivo Excel
        excel_buffer.seek(0)
        response = HttpResponse(
            excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=invoices.xlsx'
        return response


class UpdateInvoice(UpdateView):
    template_name = 'components/generic/generic_edit_invoice.html'
    form_class = CreateInvoiceForm
    model = InvoiceService.getModel()
    success_url = reverse_lazy('dashboard:invoices')

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
                return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = "Actualizar Picking"
        return context

    def form_valid(self, form):
        invoice = form.save(commit=False)
        updated_bottles_data = form.cleaned_data.get('updated_bottles', None)
        order_id = form.cleaned_data.get('order_id', None)
        status = form.cleaned_data.get('status', None)
        
        # ClientService.assignAndValidate(order_id)

        
        if status == 'approved' or status == 'approved_but_incomplete':
            ClientService.assignAndValidate(order_id)

        if updated_bottles_data:
            try:
                updated_bottles = json.loads(updated_bottles_data)
                invoice.updated_bottles = updated_bottles
            except ValueError:
                form.add_error('updated_bottles', 'Formato JSON inválido.')
                return self.form_invalid(form)
        invoice.save()
        return super().form_valid(form)


class ViewInvoice(UpdateView):
    template_name = 'components/generic/generic_edit_invoice.html'
    form_class = ViewInvoiceForm
    model = InvoiceService.getModel()
    success_url = reverse_lazy('dashboard:invoices')

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
                return HttpResponseRedirect(reverse_lazy(settings.NOT_ALLOWED))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = "Visualizar Picking"
        context['disabled_save'] = True
        return context

    def form_valid(self, form):
        invoice = form.save(commit=False)
        updated_bottles_data = form.cleaned_data.get('updated_bottles', None)
        if updated_bottles_data:
            try:
                updated_bottles = json.loads(updated_bottles_data)
                invoice.updated_bottles = updated_bottles
            except ValueError:
                form.add_error('updated_bottles', 'Formato JSON inválido.')
                return self.form_invalid(form)
        invoice.save()
        return super().form_valid(form)
