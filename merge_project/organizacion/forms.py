from django import forms

from .models import Delegacion


class DelegacionForm(forms.ModelForm):
    class Meta:
        model = Delegacion
        fields = ['nombre', 'ambito', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej.: Delegación Las Compañías',
            }),
            'ambito': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Describe el territorio o área que cubre esta delegación',
            }),
            'estado': forms.RadioSelect,
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 4:
            raise forms.ValidationError('El nombre debe tener al menos 4 caracteres.')
        return nombre
