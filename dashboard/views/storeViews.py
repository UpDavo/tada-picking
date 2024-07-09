from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, UpdateView
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from dashboard.forms import CreateStoreForm
from core.services.store_service import StoreService
from django.conf import settings

PERMISSION = 'dashboard:stores'


class StoreList(TemplateView):
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

        page_obj, fields, object_data, edit_url, delete_url, create_url, list_url = StoreService.getList(
            self.request, name)

        context['nombre'] = "Tiendas"
        context['busqueda'] = "nombre de la tienda"
        context['key'] = "onlycreate"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['edit_url'] = edit_url
        context['delete_url'] = delete_url
        context['create_url'] = create_url
        context['list_url'] = list_url

        return context


class DeleteStore(View):

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

    def post(self, request, pk):
        model = StoreService.getModel()
        item = get_object_or_404(model, pk=pk)
        item.delete()
        return redirect('dashboard:stores')


class EditStore(UpdateView):
    template_name = 'components/generic/generic_edit.html'
    form_class = CreateStoreForm
    model = StoreService.getModel()
    success_url = reverse_lazy('dashboard:stores')

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
        context['nombre'] = "Editar Tienda"
        # context['key'] = "user"
        return context


class CreateStore(TemplateView):
    template_name = 'components/generic/generic_create.html'

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
        form = CreateStoreForm()
        return render(request, self.template_name, {'form': form, 'nombre': 'Crear una Tienda', 'key': 'store'})

    def post(self, request, *args, **kwargs):
        form = CreateStoreForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse_lazy('dashboard:stores'))
        else:
            return render(request, self.template_name, {'form': form, 'nombre': 'Crear una Tienda'})
