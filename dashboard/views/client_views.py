from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponseRedirect
from dashboard.forms import CreateStoreForm
from core.services.client_service import ClientService
from django.conf import settings
import pandas as pd
from core.services.stock_service import StockService

PERMISSION = 'dashboard:clients'


class ClientList(TemplateView):
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

        page_obj, fields, object_data, list_url, upload_url = ClientService.getList(
            self.request, name)

        context['nombre'] = "Clientes"
        context['busqueda'] = "cliente"
        context['key'] = "nocreate"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['list_url'] = list_url
        context['upload_url'] = upload_url

        return context


class UploadClients(TemplateView):
    template_name = 'components/generic/upload_client_general.html'

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

    def get(self, request, *args, **kwargs):
        if 'download' in request.GET:
            return ClientService.create_excel_template2()
        return render(request, self.template_name, {'nombre': 'Cargar Clientes'})

    def post(self, request, *args, **kwargs):
        expected_cols = ['ci', 'nombre', 'email', 'celular']
        if 'file' not in request.FILES:
            return render(request, self.template_name, {'nombre': 'Cargar Clientes', 'error': True})

        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file, engine='openpyxl')

        if all(col in df.columns for col in expected_cols):
            ClientService.uploadDataframe(df)
            return HttpResponseRedirect(reverse_lazy('dashboard:clients'))
        else:
            return render(request, self.template_name, {'nombre': 'Cargar Clientes', 'error': True})
