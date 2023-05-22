from phone_verify.services import PhoneVerificationService
from phone_verify.backends import get_sms_backend
from phone_verify.models import SMSVerification
from django.contrib.contenttypes.models import ContentType
import logging


logger = logging.getLogger(__name__)


def send_security_code_and_generate_session_token(phone_number, model=None, instance_id=None, field_name=None):
    """Override this service method from phone_verify app."""
    sms_backend = get_sms_backend(phone_number)
    security_code, session_token = sms_backend.create_security_code_and_session_token(
        number=phone_number
    )
    try:
        object = SMSVerification.objects.get(security_code=security_code, session_token=session_token)
    except SMSVerification.DoesNotExist:
        pass
    # update model and instance fields
    if model:
        object.model = ContentType.objects.get(app_label=model._meta.app_label,  # pylint: disable=W0212
                                               model=model.__name__.lower())
    if instance_id:
        object.instance = instance_id
    if field_name:
        object.field_name = field_name
    object.save()
    service = PhoneVerificationService(phone_number=phone_number)
    try:
        service.send_verification(phone_number, security_code)
    except service.backend.exception_class:
        logger.error('Error in sending verification code.')
    return session_token