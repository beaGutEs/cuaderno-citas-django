"""
URLs de la app citas.

Aquí defino todas las rutas relacionadas con el contenido:
- Ver lista de contenido con filtros
- Inbox (contenido sin clasificar)
- Vista aleatoria
- Crear nuevo contenido
- Editar contenido existente
- Marcar/desmarcar favoritos
- Gestión de temas
"""

from django.urls import path
from . import views

# app_name me permite hacer referencia a estas URLs como 'citas:nombre'
# Por ejemplo: {% url 'citas:quote_list' %}
app_name = 'citas'

urlpatterns = [
    # Lista principal de contenido (con filtros)
    # URL: /citas/
    # Vista: muestra todo el contenido del usuario con opciones de filtrado
    path('', views.quote_list, name='quote_list'),
    
    # Inbox (contenido sin tema asignado)
    # URL: /citas/inbox/
    # Vista: solo muestra contenido que no tiene tema
    path('inbox/', views.quote_inbox, name='quote_inbox'),
    
    # Vista aleatoria
    # URL: /citas/random/
    # Vista: muestra un contenido aleatorio del usuario
    path('random/', views.quote_random, name='quote_random'),
    
    # Crear nuevo contenido
    # URL: /citas/create/
    # Vista: formulario para añadir contenido nuevo
    path('create/', views.quote_create, name='quote_create'),
    
    # Editar contenido existente
    # URL: /citas/edit/5/ (donde 5 es el ID)
    # <int:pk> captura el número de la URL y se lo pasa a la vista como parámetro
    # Vista: formulario precargado para editar
    path('edit/<int:pk>/', views.quote_edit, name='quote_edit'),
    
    # Marcar/desmarcar favorito
    # URL: /citas/toggle-favorite/5/
    # Vista: botón que alterna el estado de favorito
    # Solo acepta POST (no GET) por seguridad
    path('toggle-favorite/<int:pk>/', views.quote_toggle_favorite, name='quote_toggle_favorite'),
    
    # Crear nuevo tema
    # URL: /citas/tema/nuevo/
    # Vista: formulario simple para crear temas de clasificación
    path('tema/nuevo/', views.tema_create, name='tema_create'),
]