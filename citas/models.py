"""
Modelos de la app citas.

Aquí defino las "tablas" de la BD:
- Tema: para organizar las citas (Motivación, Filosofía, etc.)
- Cita: la cita en sí, con texto y/o imagen

Cada vez que cambio algo aquí tengo que hacer:
python manage.py makemigrations
python manage.py migrate
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Tema(models.Model):
    """
    Modelo para los temas/tags.
    
    Sirve para clasificar las citas.
    Por ejemplo: "Motivación", "Filosofía", "Cine"
    
    Cada usuario tiene sus propios temas, no se comparten.
    """
    
    # Quién creó este tema
    # ForeignKey = muchos temas pertenecen a un usuario
    # on_delete=CASCADE: si borro el usuario, se borran sus temas
    # related_name='temas': para hacer user.temas.all()
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='temas'
    )
    
    # Nombre del tema
    # CharField = texto corto (máximo 50 caracteres)
    name = models.CharField(max_length=50, verbose_name='Nombre del tema')
    
    # Cuándo se creó
    # auto_now_add=True: se rellena solo al crear
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
        
        # Por defecto los ordena alfabéticamente por nombre
        ordering = ['name']
        
        # Un usuario no puede tener dos temas con el mismo nombre
        # Pero dos usuarios SÍ pueden tener temas llamados igual
        unique_together = ['owner', 'name']
    
    
    def __str__(self):
        # Esto es lo que se muestra en el admin y en los selects
        return self.name


class Cita(models.Model):
    """
    Modelo para las citas.
    
    Una cita puede tener:
    - Solo texto
    - Solo imagen
    - Texto + imagen
    
    Pero NO puede estar vacía (ni texto ni imagen).
    Eso lo valido en clean() y en el formulario.
    """
    
    # Quién creó esta cita
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='citas'
    )
    
    # El texto de la cita
    # TextField = texto largo sin límite
    # blank=True: puede estar vacío (si hay imagen)
    text = models.TextField(blank=True, verbose_name='Texto de la cita')
    
    # Imagen de la cita
    # ImageField = para subir imágenes
    # upload_to='quotes/': las guarda en media/quotes/
    # blank=True, null=True: es opcional
    # OJO: Necesita Pillow instalado
    image = models.ImageField(
        upload_to='quotes/', 
        blank=True, 
        null=True, 
        verbose_name='Imagen'
    )
    
    # De dónde viene la cita (autor, libro, etc.)
    # Es opcional
    source = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name='Fuente'
    )
    
    # Tema de la cita
    # ForeignKey a Tema (opcional)
    # null=True, blank=True: puede no tener tema
    # on_delete=SET_NULL: si borro el tema, la cita se queda sin tema (no se borra)
    tag = models.ForeignKey(
        Tema, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='citas', 
        verbose_name='Tema'
    )
    
    # Si es favorita o no
    # BooleanField = True/False
    # default=False: por defecto no es favorita
    is_favorite = models.BooleanField(default=False, verbose_name='Favorito')
    
    # Cuándo se creó
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Cuándo se editó por última vez
    # auto_now=True: se actualiza automáticamente cada vez que guardo
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        
        # Las más recientes primero
        # '-created_at' = orden descendente
        ordering = ['-created_at']
    
    
    def __str__(self):
        # Si tiene texto, muestro los primeros 50 caracteres
        if self.text:
            texto_corto = self.text[:50]
            if len(self.text) > 50:
                texto_corto += '...'
            return texto_corto
        
        # Si solo tiene imagen, muestro esto
        return f"Cita con imagen ({self.id})"
    
    
    def clean(self):
        """
        Validación personalizada.
        
        Compruebo que tenga AL MENOS texto o imagen.
        Si no tiene ninguno, lanzo error.
        
        Django llama a esto automáticamente cuando uso formularios.
        """
        super().clean()
        
        # Si NO tiene texto Y NO tiene imagen
        if not self.text and not self.image:
            raise ValidationError(
                'La cita debe tener al menos texto o una imagen.'
            )