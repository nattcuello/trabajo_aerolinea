from rest_framework.routers import DefaultRouter
from .views_api import PerfilUsuarioViewSet

app_name = "usuarios"

router = DefaultRouter()
router.register(r"perfiles", PerfilUsuarioViewSet, basename="perfil-usuario")

urlpatterns = router.urls
