from rest_framework import routers
from data.controllers.document import DocumentViewSet
from django.conf import settings
from django.conf.urls.static import static
from data.controllers.user import VerificationViewSet
from data.controllers.city import CityViewSet, CountryViewSet
from data.controllers.user import UploadPhotoViewSet
from data.controllers.company import CompanyViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r'upload-document', DocumentViewSet)
ROUTER.register(r'phone', VerificationViewSet, basename='phone')
ROUTER.register(r'cities', CityViewSet)
ROUTER.register(r'countries', CountryViewSet)
ROUTER.register(r'photo', UploadPhotoViewSet, basename='photo')
ROUTER.register(r'company', CompanyViewSet, basename='company')


urlpatterns = ROUTER.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)