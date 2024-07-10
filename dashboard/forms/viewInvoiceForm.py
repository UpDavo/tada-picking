from django import forms
from core.models import Invoice, Bottle
import json

class ViewInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['status', 'approval_comment', 'product_photo']
        labels = {
            'status': 'Estado',
            'approval_comment': 'Comentario de Aprobación',
            'product_photo': 'Foto del Producto',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'select select-bordered select-primary w-full rounded', 'disabled': 'disabled'}),
            'approval_comment': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Comentario de aprobación', 'disabled': 'disabled'}),
            'product_photo': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered file-input-primary w-full rounded', 'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super(ViewInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = Invoice.STATUS_CHOICES

        # Obtener todas las botellas disponibles
        self.bottles = Bottle.objects.all()
        for bottle in self.bottles:
            # Campos para las botellas actuales (Motorizado) - deshabilitados
            self.fields[f'motorizado_bottle_{bottle.id}'] = forms.IntegerField(
                label=f'Motorizado: {bottle.type}',
                required=False,
                initial=self.instance.bottles.get(str(bottle.id), 0),
                widget=forms.NumberInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'disabled': 'disabled'})
            )
            # Campos para las botellas actualizadas (POC) - deshabilitados
            self.fields[f'poc_bottle_{bottle.id}'] = forms.IntegerField(
                label=f'POC: {bottle.type}',
                required=False,
                initial=self.instance.updated_bottles.get(str(bottle.id), 0) if self.instance.updated_bottles else 0,
                widget=forms.NumberInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'disabled': 'disabled'})
            )

    def save(self, commit=True):
        invoice = super().save(commit=False)
        updated_bottles = {}

        # Actualizar las cantidades de botellas (esto no se ejecutará porque los campos están deshabilitados, pero se mantiene por consistencia)
        for bottle in self.bottles:
            poc_field_name = f'poc_bottle_{bottle.id}'
            poc_quantity = self.cleaned_data.get(poc_field_name)

            if poc_quantity is not None:
                updated_bottles[str(bottle.id)] = poc_quantity

        invoice.updated_bottles = updated_bottles
        if commit:
            invoice.save()
        return invoice
