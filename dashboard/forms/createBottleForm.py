from django import forms
from core.models import Bottle


class CreateBottleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateBottleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bottle
        fields = ['type', 'image', 'min_bottles', 'bottle_range']
        labels = {
            'type': 'Nombre de la Botella',
            'min_bottles': 'Mínimo de botellas',
            'bottle_range': 'Rango de botellas',
            'image': 'Fotografía de la botella',
        }
        widgets = {
            'type': forms.TextInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded',
                'placeholder': 'Nombre de la Botella'
            }),
            'min_bottles': forms.NumberInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded',
                'placeholder': 'Mínimo de botellas'
            }),
            'bottle_range': forms.NumberInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded',
                'placeholder': 'Rango de botellas'
            }),
            'image': forms.FileInput(attrs={
                'class': 'file-input file-input-primary file-input-bordered w-full rounded', 'placeholder': 'Imágen del producto'}),
        }
