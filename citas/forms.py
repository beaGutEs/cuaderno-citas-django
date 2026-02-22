"""
Formularios de la app citas.

Tengo dos formularios:
1. QuoteFilterForm: para filtrar la lista (Form normal)
2. QuoteForm: para crear/editar citas (ModelForm)

La diferencia:
- Form: formulario genérico, no guarda nada en BD
- ModelForm: basado en un modelo, guarda en BD
"""

from django import forms
from .models import Cita, Tema


class QuoteFilterForm(forms.Form):
    """
    Formulario para filtrar citas.
    
    No guarda nada, solo sirve para construir los filtros.
    Los datos vienen en la URL como parámetros GET.
    
    Campos:
    - q: buscador de texto
    - favorite_only: checkbox "solo favoritas"
    - with_image_only: checkbox "solo con imagen"
    - tag: selector de tema
    """
    
    # Campo de búsqueda
    # required=False: no es obligatorio rellenarlo
    # widget: personalizo el input HTML
    q = forms.CharField(
        required=False, 
        label='Buscar',
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar en texto o fuente...',
            'class': 'form-control'
        })
    )
    
    # Checkbox para filtrar solo favoritas
    # Los BooleanField son checkboxes
    favorite_only = forms.BooleanField(
        required=False, 
        label='Solo favoritas'
    )
    
    # Checkbox para filtrar solo con imagen
    with_image_only = forms.BooleanField(
        required=False, 
        label='Solo con imagen'
    )
    
    # Select de temas
    # ModelChoiceField = select con opciones de un modelo
    # queryset lo relleno en __init__ porque depende del usuario
    tag = forms.ModelChoiceField(
        queryset=Tema.objects.none(),  # De momento vacío
        required=False,
        empty_label='Todos los temas',
        label='Tema',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    
    def __init__(self, *args, **kwargs):
        """
        Constructor personalizado.
        
        Necesito recibir el usuario para filtrar los temas.
        Solo quiero mostrar los temas del usuario actual, no los de otros.
        
        Uso: QuoteFilterForm(request.GET, user=request.user)
        """
        # Saco el parámetro 'user' de kwargs
        # pop() lo extrae para que no llegue a super().__init__()
        user = kwargs.pop('user', None)
        
        # Llamo al __init__ original
        super().__init__(*args, **kwargs)
        
        # Si me pasaron un usuario
        if user:
            # Filtro los temas solo del usuario actual
            # Sobrescribo el queryset del campo 'tag'
            self.fields['tag'].queryset = Tema.objects.filter(owner=user)


class QuoteForm(forms.ModelForm):
    """
    Formulario para crear y editar citas.
    
    Es un ModelForm porque está basado en el modelo Cita.
    Django automáticamente:
    - Crea campos para text, image, source, etc.
    - Sabe cómo guardar en la BD
    - Aplica las validaciones del modelo
    
    Yo añado:
    - Validación extra en clean()
    - Filtrado de temas por usuario
    - Widgets personalizados
    """
    
    class Meta:
        # Modelo asociado
        model = Cita
        
        # Campos que incluyo en el formulario
        # NO incluyo owner (lo asigno en la vista)
        # NO incluyo created_at ni updated_at (son automáticos)
        fields = ['text', 'image', 'source', 'tag', 'is_favorite']
        
        # Personalizo cómo se renderizan algunos campos
        widgets = {
            # text: textarea en vez de input
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribe la cita aquí...',
                'class': 'form-control'
            }),
            
            # source: input con placeholder
            'source': forms.TextInput(attrs={
                'placeholder': 'Autor, libro, película...',
                'class': 'form-control'
            }),
        }
    
    
    def __init__(self, *args, **kwargs):
        """
        Constructor personalizado.
        
        Similar a QuoteFilterForm, necesito el usuario para:
        1. Filtrar los temas (solo los del usuario)
        2. Cambiar el texto de la opción vacía del select
        
        Uso: QuoteForm(user=request.user)
        """
        # Extraigo el parámetro 'user'
        user = kwargs.pop('user', None)
        
        # Llamo al __init__ de ModelForm
        super().__init__(*args, **kwargs)
        
        # Si hay usuario
        if user:
            # Solo muestro los temas del usuario actual
            self.fields['tag'].queryset = Tema.objects.filter(owner=user)
            
            # Cambio el texto de la opción vacía
            # Por defecto sería "-------" que no es muy descriptivo
            self.fields['tag'].empty_label = 'Sin clasificar (irá al Inbox)'
    
    
    def clean(self):
        """
        Validación personalizada.
        
        Compruebo que haya AL MENOS texto o imagen.
        Si no hay ninguno, lanzo error y el formulario no se guarda.
        
        El error se muestra arriba del formulario en el template.
        """
        # Primero ejecuto la validación normal (required, max_length, etc.)
        cleaned_data = super().clean()
        
        # Obtengo los valores limpios de text e image
        text = cleaned_data.get('text')
        image = cleaned_data.get('image')
        
        # Si NO hay texto Y NO hay imagen
        # not text: True si text es vacío o None
        # not image: True si image es None (no se subió archivo)
        if not text and not image:
            # Lanzo error de validación
            raise forms.ValidationError(
                'Debes añadir al menos texto o una imagen. La cita no puede estar vacía.'
            )
        
        # Devuelvo los datos limpios
        # Es importante devolverlos
        return cleaned_data