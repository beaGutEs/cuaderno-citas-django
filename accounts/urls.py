"""
URLs de autenticación.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registro de nuevos usuarios
    path('register/', views.register, name='register'),
    
    # Login
    path('login/', views.login_view, name='login'),
    
    # Logout
    path('logout/', views.logout_view, name='logout'),
]