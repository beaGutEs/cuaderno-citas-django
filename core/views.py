"""
Vistas de la app core.

Son las páginas públicas del sitio (home y about).
Súper simples, solo renderean templates sin más lógica.
"""

from django.shortcuts import render


def home(request):
    """
    Página de inicio.
    
    Es lo primero que ve la gente cuando entra al sitio.
    Muestro info del proyecto y enlaces para registrarse o entrar.
    
    No necesita @login_required porque es pública.
    """
    return render(request, 'core/home.html')


def about(request):
    """
    Página "sobre el proyecto".
    
    Explico qué es esto, qué tecnologías usé, etc.
    También pública, cualquiera puede verla.
    """
    return render(request, 'core/about.html')