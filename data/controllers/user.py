from django.contrib.auth.models import User
from phone_verify.api import VerificationViewSet as VerifyViewSET
from phone_verify.base import response
from phone_verify.serializers import PhoneSerializer
from data.services.utils import send_security_code_and_generate_session_token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,mixins
from ..serializers.user_serializer import UploadPhotoSerializer
from rest_framework.response import Response
from rest_framework import status
from data.models.user_model import Profile

class VerificationViewSet(VerifyViewSET):
    """
    API endpoint for phone verification. Inherited from phone_verify app.
    """
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        serializer_class=PhoneSerializer,
    )
    def register(self, request):
        """
        Send an sms with verification code to the connected user.
        """
        # TODO: Use service implementation  # pylint: disable=W0511
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = str(serializer.validated_data["phone_number"])
        if hasattr(request.user, 'profile'):
            user_phone_number = request.user.profile.phone
        else:
            return response.Ok({"error": "User doesn't have a phone number!"})
        if user_phone_number != phone_number:
            return response.Ok({"error": 'You have entered the wrong phone number!'})
        if not request.user.profile.phone_is_verified:
            session_token = send_security_code_and_generate_session_token(
                phone_number=str(phone_number),
                model=User,
                instance_id=self.request.user.id,
                field_name='phone_number'
            )
            return response.Ok({"session_token": session_token})
        return response.Ok({"phone_number": f'Your number {phone_number} is already verified!'})

class UploadPhotoViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UploadPhotoSerializer
    permission_classes=[IsAuthenticated,]
    queryset = Profile.objects.all()