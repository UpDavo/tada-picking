from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import HttpResponseRedirect
from core.services.invoice_service import InvoiceService
from django.conf import settings
from dashboard.forms import CreateInvoiceForm, ViewInvoiceForm
import json

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

        name = self.request.GET.get('name')

        page_obj, fields, object_data, list_url, description_url, view_url = InvoiceService.getInvoiceList(
            self.request, name)

        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Picking"
        context['busqueda'] = "número de orden"
        context['fields'] = fields
        # context['delete_url'] = 'dashboard:invoice_description'
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['description_url'] = description_url
        context['view_url'] = view_url
        context['list_url'] = list_url

        return context
    
    
class UpdateInvoice(UpdateView):
    template_name = 'components/generic/generic_edit.html'
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
    template_name = 'components/generic/generic_edit.html'
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
        context['nombre'] = "Actualizar Picking"
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