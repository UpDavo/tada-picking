from django import forms
from core.models import Bottle


class CreateBottleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateBottleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bottle
        fields = ['type', 'min_bottles', 'image']
        labels = {
            'type': 'Nombre de la Botella',
            'min_bottles': 'Mínimo de botellas',
            'image': 'Fotografía de la botella',
        }
        widgets = {
            'type': forms.TextInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded',
                'placeholder': 'Nombre de la Botella'
            }),
            'min_bottles': forms.NumberInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded',
                'placeholder': 'Nombre de la Botella'
            }),
            'image': forms.FileInput(attrs={
                'class': 'file-input file-input-primary file-input-bordered w-full rounded', 'placeholder': 'Imágen del producto'}),
        }
