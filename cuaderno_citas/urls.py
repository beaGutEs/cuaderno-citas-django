"""
URLs principales del proyecto.

Aquí conecto las URLs de cada app.
También configuro servir archivos media en desarrollo.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),
    
    # URLs de core (home y about)
    # Como no tiene prefijo, '' significa que van en la raíz
    # Ejemplo: / → home, /about/ → about
    path('', include('core.urls')),
    
    # URLs de accounts (autenticación)
    # Prefijo 'accounts/' → /accounts/login/, /accounts/register/, etc.
    path('accounts/', include('accounts.urls')),
    
    # URLs de citas (app principal)
    # Prefijo 'citas/' → /citas/, /citas/create/, etc.
    path('citas/', include('citas.urls')),
]

# En desarrollo, sirvo archivos media (imágenes subidas)
# En producción esto lo haría Nginx o Apache, no Django
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)