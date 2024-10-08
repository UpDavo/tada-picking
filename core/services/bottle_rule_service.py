from django.core.paginator import Paginator
from core.models import PackRule, BottleQuantity
from django.db import models
# from django.urls import reverse_lazy


class BottleRuleService:

    @staticmethod
    def getList(request, name):
        # Obtener todos los PackRules
        items = PackRule.objects.order_by('created_at').all()

        if name:
            items = items.filter(type__icontains=name)

        # Obtener los campos del modelo PackRule como una lista de objetos Field
        fields = PackRule._meta.fields
        fields_to_include = ['id', 'created_at', 'name', 'product']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los resultados
        paginator = Paginator(items, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        list_url = 'dashboard:bottle_rules'
        edit_url = 'dashboard:bottle_rule_edit'
        delete_url = 'dashboard:bottle_rule_delete'
        create_url = 'dashboard:bottle_rule_create'

        # Obtener los valores de los campos para cada PackRule
        object_data = []
        for obj in page_obj:
            # Obtener los valores de los campos definidos en 'fields'
            obj_data = [getattr(obj, field.name) for field in fields]

            # Obtener las botellas y sus cantidades relacionadas con el PackRule
            bottle_quantities = BottleQuantity.objects.filter(pack_rule=obj)

            # Formatear la salida en "cantidad nombre"
            bottles_info = "; ".join([f"{bottle_quantity.quantity} {bottle_quantity.bottle.type}"
                                      for bottle_quantity in bottle_quantities])

            # Agregar las botellas formateadas a los datos del objeto
            obj_data.append(bottles_info)

            object_data.append(obj_data)

        # Añadir "bottles_info" como parte de los campos mostrados
        fields.append(models.Field(name='bottles_info',
                      verbose_name='Bottle Info'))

        return page_obj, fields, object_data, edit_url, delete_url, create_url, list_url

    @staticmethod
    def checkExists(item):
        exists = PackRule.objects.filter(name=item).exists()
        return exists

    @staticmethod
    def getModel():
        return PackRule

    @staticmethod
    def getAllCities():
        return PackRule.objects.all()
