from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import ProductsView

router = DefaultRouter()
router.register(r'products', ProductsView, basename='product')
urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
