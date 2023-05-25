"""Here utils functions"""
import logging
import os
from contextlib import suppress
from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _  # pylint: disable=E0611

from phone_verify.backends import get_sms_backend
from phone_verify.models import SMSVerification
from phone_verify.services import PhoneVerificationService

logger = logging.getLogger(__name__)


def send_email(template, subject, ctx, user):
    """method to send email template"""
    html_content = render_to_string(template_name=template, context=ctx)
    msg = EmailMultiAlternatives(
        _(subject),
        html_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    attach_email_icons(msg, settings.IMAGES)
    msg.send(fail_silently=True)


def attach_email_icons(msg, images):
    """method to attach icons to email template"""
    msg.mixed_subtype = "related"
    for image in images:
        file_path = os.path.join(image[0], image[1])
        with open(file_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<{name}>".format(name=image[1]))
            img.add_header("Content-Disposition", "inline", filename=image[1])
        msg.attach(img)


def send_security_code_and_generate_session_token(
    phone_number, model=None, instance_id=None, field_name=None
):
    """Override this service method from phone_verify app."""
    sms_backend = get_sms_backend(phone_number)
    security_code, session_token = sms_backend.create_security_code_and_session_token(
        number=phone_number
    )
    with suppress(SMSVerification.DoesNotExist):
        obj = SMSVerification.objects.get(security_code=security_code, session_token=session_token)
    # update model and instance fields
    if model:
        obj.model = ContentType.objects.get(
            app_label=model._meta.app_label, model=model.__name__.lower()  # pylint: disable=W0212
        )
    if instance_id:
        obj.instance = instance_id
    if field_name:
        obj.field_name = field_name
    obj.save()
    service = PhoneVerificationService(phone_number=phone_number)
    try:
        service.send_verification(phone_number, security_code)
    except service.backend.exception_class:
        logger.error("Error in sending verification code.")
    return session_token
