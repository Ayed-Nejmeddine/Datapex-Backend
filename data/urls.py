from rest_framework import routers
from data.controllers.document import DocumentViewSet
from django.conf import settings
from django.conf.urls.static import static


ROUTER = routers.DefaultRouter()
ROUTER.register(r'upload-document', DocumentViewSet)

urlpatterns = ROUTER.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)