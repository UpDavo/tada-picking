# forms.py
from django import forms
from core.models import Invoice, Bottle

class CreatePickingForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'order_id',
            'store',
            'description',
            'product_photo',
        ]
        labels = {
            'order_id': 'ID del Pedido',
            'store': 'Tienda',
            'description': 'Descripción',
            'product_photo': 'Foto del Producto',
        }
        widgets = {
            'order_id': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'ID del Pedido'}),
            'store': forms.Select(attrs={'class': 'input input-bordered input-primary w-full rounded'}),
            'description': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Descripción'}),
            'product_photo': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered file-input-primary w-full rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreatePickingForm, self).__init__(*args, **kwargs)
        self.fields['order_id'].disabled = True
        self.fields['description'].required = False