from rest_framework import routers
from data.views import FileViewSet
from django.conf import settings
from django.conf.urls.static import static


ROUTER = routers.DefaultRouter()
ROUTER.register(r'files', FileViewSet)

urlpatterns = ROUTER.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)