"""Here user controller"""
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode

from phone_verify.api import VerificationViewSet as VerifyViewSET
from phone_verify.base import response
from phone_verify.serializers import PhoneSerializer
from rest_auth.views import PasswordResetConfirmView
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from data.models.user_model import Profile
from data.serializers.user_serializer import UploadPhotoSerializer
from data.services.utils import send_email
from data.services.utils import send_security_code_and_generate_session_token


class VerificationViewSet(VerifyViewSET):  # pylint: disable=R0903
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
        if hasattr(request.user, "profile"):
            user_phone_number = request.user.profile.phone
        else:
            return response.Ok({"error": "User doesn't have a phone number!"})
        if user_phone_number != phone_number:
            return response.Ok({"error": "You have entered the wrong phone number!"})
        if not request.user.profile.phone_is_verified:
            session_token = send_security_code_and_generate_session_token(
                phone_number=str(phone_number),
                model=User,
                instance_id=self.request.user.id,
                field_name="phone_number",
            )
            return response.Ok({"session_token": session_token})
        return response.Ok({"phone_number": f"Your number {phone_number} is already verified!"})


class UploadPhotoViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):  # pylint: disable=R0903
    """View for uploading user photo"""

    serializer_class = UploadPhotoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Profile.objects.all()


class CustomPasswordResetConfirmView(PasswordResetConfirmView):  # pylint: disable=R0903
    """Override of PasswordResetConfirmView"""

    def post(self, request, *args, **kwargs):
        """Override of post method"""
        resp = super().post(request, *args, **kwargs)
        uidb64 = request.data["uid"]
        uid = urlsafe_base64_decode(uidb64).decode("utf-8")
        user = User.objects.get(pk=uid)
        password_change_time = timezone.now()
        ctx = {
            "username": user.first_name,
            "email": user.email,
            "date": password_change_time.date(),
            "time": password_change_time.time(),
        }
        send_email("modification_mot_passe.html", "Your password has been changed", ctx, user)
        return resp
