from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # 💡 importante para servir estáticos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vuelos/', include('vuelos.urls')),
    path('pasajeros/', include('pasajeros.urls')),
    path('reservas/', include('reservas.urls')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('', include('home.urls')),
]

# ✅ Esto sirve archivos estáticos en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
