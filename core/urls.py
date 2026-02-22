"""
URLs de la app core.
"""

from django.urls import path
from . import views

# app_name para hacer referencia como 'core:home' en los templates
app_name = 'core'

urlpatterns = [
    # Página de inicio (raíz del sitio)
    path('', views.home, name='home'),
    
    # Página about
    path('about/', views.about, name='about'),
]