from pyexpat import model
from django import forms

from icarusProjectApp.models import (
    Usuario,
    Pago,
)

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        widgets = {
            'password': forms.PasswordInput(),
        }

