from django import forms
from core.models import Bottle

class CreateBottleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateBottleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bottle
        fields = ['type']
        labels = {
            'type': 'Nombre de la Botella',
        }
        widgets = {
            'type': forms.TextInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded', 
                'placeholder': 'Nombre de la Botella'
            }),
        }