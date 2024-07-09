from django import forms
from core.models import Store, City

class CreateStoreForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateStoreForm, self).__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.all()

    class Meta:
        model = Store
        fields = ['name', 'city']
        labels = {
            'name': 'Nombre de la Tienda',
            'city': 'Ciudad',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded', 
                'placeholder': 'Nombre de la Tienda'
            }),
            'city': forms.Select(attrs={
                'class': 'input input-bordered input-primary w-full rounded', 
                'placeholder': 'Ciudad'
            }),
        }
