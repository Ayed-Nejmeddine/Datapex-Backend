"""Data api urls"""
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from data.controllers.city import CityViewSet
from data.controllers.city import CountryViewSet
from data.controllers.company import CompanyViewSet
from data.controllers.document import CleanedDocumentViewSet
from data.controllers.document import DocumentViewSet
from data.controllers.user import EmailConfirmationViewSet
from data.controllers.user import UploadPhotoViewSet
from data.controllers.user import VerificationViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r"upload-document", DocumentViewSet)
ROUTER.register(r"clean-document", CleanedDocumentViewSet)
ROUTER.register(r"phone", VerificationViewSet, basename="phone")
ROUTER.register(r"cities", CityViewSet)
ROUTER.register(r"countries", CountryViewSet)
ROUTER.register(r"photo", UploadPhotoViewSet, basename="photo")
ROUTER.register(r"company", CompanyViewSet, basename="company")
ROUTER.register(r"email", EmailConfirmationViewSet, basename="email")

urlpatterns = ROUTER.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
