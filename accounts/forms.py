"""
Formularios de autenticación.

Solo tengo uno personalizado: RegisterForm.
Para login uso directamente AuthenticationForm de Django.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Formulario de registro.
    
    Extiendo UserCreationForm (que trae Django) para añadir email obligatorio.
    Por defecto UserCreationForm solo pide username y password, y el email es opcional.
    
    Yo quiero que el email sea obligatorio por si luego implemento recuperación de contraseña.
    """
    
    # Añado el campo email
    # EmailField valida que sea un email válido
    # required=True: obligatorio
    email = forms.EmailField(
        required=True, 
        help_text='Necesitamos tu email para la cuenta.'
    )
    
    class Meta:
        # Modelo asociado (User viene de django.contrib.auth)
        model = User
        
        # Campos que incluyo en el formulario
        # username y password1/password2 vienen de UserCreationForm
        # email lo añado yo
        fields = ['username', 'email', 'password1', 'password2']
    
    
    def save(self, commit=True):
        """
        Guardo el usuario con el email.
        
        Sobrescribo save() para asegurarme de que el email se guarda.
        commit=False: no lo guardo todavía en BD
        commit=True: lo guardo en BD (comportamiento por defecto)
        """
        # Llamo al save() original pero sin guardar todavía
        user = super().save(commit=False)
        
        # Asigno el email del formulario al usuario
        user.email = self.cleaned_data['email']
        
        # Si commit=True, guardo en BD
        if commit:
            user.save()
        
        return user