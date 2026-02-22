"""
Configuración del admin para la app citas.

Registro los modelos Tema y Cita para poder gestionarlos desde /admin/
"""

from django.contrib import admin
from .models import Tema, Cita


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Tema.
    
    Personalizo qué columnas se ven, qué se puede buscar, etc.
    """
    
    # Columnas que se muestran en la lista
    list_display = ['name', 'owner', 'created_at']
    
    # Campos por los que se puede buscar
    search_fields = ['name', 'owner__username']
    
    # Filtros laterales
    list_filter = ['created_at']


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Cita.
    
    Aquí añado un método personalizado (get_preview) para mostrar
    un preview del texto en la lista.
    """
    
    # Columnas que se muestran
    # get_preview es un método que creo abajo
    list_display = ['id', 'get_preview', 'source', 'tag', 'is_favorite', 'owner', 'created_at']
    
    # Campos por los que se puede buscar
    search_fields = ['text', 'source', 'owner__username']
    
    # Filtros laterales
    list_filter = ['is_favorite', 'tag', 'created_at']
    
    # Campos que no se pueden editar (solo ver)
    readonly_fields = ['created_at', 'updated_at']
    
    
    def get_preview(self, obj):
        """
        Método personalizado para mostrar un preview del texto.
        
        Si tiene texto, muestro los primeros 50 caracteres.
        Si solo tiene imagen, muestro [Con imagen].
        Si no tiene nada (bug), muestro [Vacía].
        """
        if obj.text:
            # Si el texto es largo, lo corto y añado "..."
            if len(obj.text) > 50:
                return obj.text[:50] + '...'
            return obj.text
        elif obj.image:
            return '[Con imagen]'
        return '[Vacía]'
    
    # short_description es el título de la columna en el admin
    get_preview.short_description = 'Preview'