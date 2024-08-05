from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, UpdateView
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from dashboard.forms import PackRuleForm
from core.services.bottle_rule_service import BottleRuleService
from django.conf import settings
from core.models import BottleQuantity, PackRule

PERMISSION = 'dashboard:bottle_rules'


class BottleRuleList(TemplateView):
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

        page_obj, fields, object_data, edit_url, delete_url, create_url, list_url = BottleRuleService.getList(
            self.request, name)

       # Pasar los datos de los objetos y los campos al contexto
        # Pasar los datos de los objetos y los campos al contexto
        context['nombre'] = "Reglas"
        context['busqueda'] = "nombre de la regla"
        context['key'] = "onlycreate"
        context['fields'] = fields
        context['object_data'] = object_data
        context['page_obj'] = page_obj
        context['edit_url'] = edit_url
        context['delete_url'] = delete_url
        context['create_url'] = create_url
        context['list_url'] = list_url

        return context


class DeleteBottleRule(View):

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
        model = BottleRuleService.getModel()
        item = get_object_or_404(model, pk=pk)
        item.delete()
        return redirect('dashboard:bottles')


class EditBottleRule(UpdateView):
    template_name = 'components/generic/generic_edit_rule.html'
    form_class = PackRuleForm
    model = PackRule
    success_url = reverse_lazy('dashboard:bottle_rules')

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
        context['nombre'] = "Editar Regla"
        return context

    def form_valid(self, form):
        pack_rule = form.save()  # Guarda el PackRule editado

        # Clear existing bottle quantities
        BottleQuantity.objects.filter(pack_rule=pack_rule).delete()

        # Save updated bottle quantities if not a general rule
        if not pack_rule.is_general:
            bottles = self.request.POST.getlist('bottles')
            for bottle_id in bottles:
                quantity_field_name = f'bottle_{bottle_id}_quantity'
                quantity = self.request.POST.get(quantity_field_name, 0)
                if int(quantity) > 0:
                    BottleQuantity.objects.create(
                        pack_rule=pack_rule,
                        bottle_id=bottle_id,
                        quantity=quantity
                    )

        return HttpResponseRedirect(self.success_url)


class CreateBottleRule(TemplateView):
    template_name = 'components/generic/generic_create_rule.html'

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
        form = PackRuleForm()
        return render(request, self.template_name, {'form': form, 'nombre': 'Crear una Regla', 'key': 'rule'})

    def post(self, request, *args, **kwargs):
        form = PackRuleForm(request.POST)
        if form.is_valid():
            # Save PackRule
            pack_rule = form.save(commit=False)
            pack_rule.save()  # Ensure the PackRule is saved before creating related objects

            # Save bottle quantities if not a general rule
            if not pack_rule.is_general:
                bottles = request.POST.getlist('bottles')
                for bottle_id in bottles:
                    quantity_field_name = f'bottle_{bottle_id}_quantity'
                    quantity = request.POST.get(quantity_field_name, 0)
                    if int(quantity) > 0:
                        BottleQuantity.objects.create(
                            pack_rule=pack_rule,
                            bottle_id=bottle_id,
                            quantity=quantity
                        )

            # Save the ManyToManyField relations
            form.save_m2m()

            return HttpResponseRedirect(reverse_lazy('dashboard:bottle_rules'))
        else:
            return render(request, self.template_name, {'form': form, 'nombre': 'Crear una Regla'})
