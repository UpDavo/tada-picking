from django.core.paginator import Paginator
from core.models import Invoice, Bottle
from django.db.models import JSONField
import pandas as pd
import json

class InvoiceService:

    @staticmethod
    def getInvoiceList(request, order_id):

        # Obtener todos los horarios del usuario actual
        invoices = Invoice.objects.filter(store=request.user.store).order_by('-created_at')

        if order_id:
            invoices = invoices.filter(order_id__icontains=order_id)

        # Obtener los campos del modelo Pais
        fields = Invoice._meta.fields
        fields_to_include = ['id', 'created_at',
                             'store', 'order_id', 'status']
        fields = [field for field in fields if field.name in fields_to_include]

        # Paginar los horarios
        paginator = Paginator(invoices, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Definir la URL de edición
        list_url = 'dashboard:invoices'
        description_url = 'dashboard:invoice_edit'
        view_url = 'dashboard:invoice_view'

        # Obtener los valores de los campos para cada objeto
        object_data = []
        for obj in page_obj:
            obj_data = [getattr(obj, field.name) for field in fields]
            object_data.append(obj_data)

        return page_obj, fields, object_data, list_url, description_url, view_url
    
    @staticmethod
    def get_excel_data(request, order_id=None):
        # Obtener todos los horarios del usuario actual
        invoices = Invoice.objects.filter(store=request.user.store).order_by('-created_at')

        if order_id:
            invoices = invoices.filter(order_id__icontains=order_id)

        # Obtener todos los campos del modelo Invoice
        fields = Invoice._meta.fields

        # Paginar los horarios
        paginator = Paginator(invoices, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Obtener los valores de los campos para cada objeto
        object_data = []
        for obj in page_obj:
            obj_data = {field.name: getattr(obj, field.name) for field in fields}
            object_data.append(obj_data)

        # Convertir object_data a DataFrame
        df = pd.DataFrame(object_data)

        # Obtener los tipos de botellas
        bottle_types = {str(bottle.id): bottle.type for bottle in Bottle.objects.all()}

        # Identificar los campos JSON y expandirlos
        json_fields = [field.name for field in fields if isinstance(field, JSONField)]

        for field in json_fields:
            # Expandir cada campo JSON
            json_col_df = df[field].apply(lambda x: pd.json_normalize(x) if pd.notnull(x) else pd.DataFrame())
            json_col_df = pd.concat(json_col_df.values.tolist()).reset_index(drop=True)

            # Renombrar las columnas con los tipos de botellas
            json_col_df.rename(columns=bottle_types, inplace=True)

            # Añadir prefijo al nombre de la columna
            json_col_df = json_col_df.add_prefix(f"{field}_")

            # Concatenar el DataFrame expandido con el original
            df = pd.concat([df.drop(columns=[field]), json_col_df], axis=1)

        # Convertir las columnas datetime a timezone unaware
        for col in df.select_dtypes(include=['datetime64[ns, UTC]', 'datetime64[ns]']).columns:
            df[col] = df[col].dt.tz_localize(None)

        return df

    @staticmethod
    def checkExists(order_id):
        exists = Invoice.objects.filter(order_id=order_id).exists()
        return exists

    @staticmethod
    def getModel():
        return Invoice
