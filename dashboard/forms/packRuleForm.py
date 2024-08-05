from django import forms
from core.models import PackRule, Bottle


class PackRuleForm(forms.ModelForm):
    class Meta:
        model = PackRule
        fields = ['name', 'product', 'is_general', 'general_quantity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded',
                'placeholder': 'Nombre de la regla'
            }),
            'product': forms.Select(attrs={
                'class': 'select select-bordered select-primary w-full rounded'
            }),
            'is_general': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            }),
            'general_quantity': forms.NumberInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded',
                'placeholder': 'Cantidad general'
            }),
        }

    bottles = forms.ModelMultipleChoiceField(
        queryset=Bottle.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'checkbox checkbox-primary'
        }),
        required=False  # Cambiado a False para permitir reglas generales sin botellas específicas
    )

    def __init__(self, *args, **kwargs):
        super(PackRuleForm, self).__init__(*args, **kwargs)

        # Añadir campos de cantidad para cada botella solo si la regla no es general
        if not self.instance.is_general:
            for bottle in Bottle.objects.all():
                self.fields[f'bottle_{bottle.id}_quantity'] = forms.IntegerField(
                    label=f'Cantidad para {bottle.type}',
                    min_value=0,
                    initial=0,
                    widget=forms.NumberInput(attrs={
                        'class': 'input input-bordered input-primary w-full rounded',
                        'placeholder': f'Cantidad para {bottle.type}'
                    })
                )

    def save(self, commit=True):
        pack_rule = super(PackRuleForm, self).save(commit=commit)
        return pack_rule
