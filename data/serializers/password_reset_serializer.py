"""Here we have password reset  serializer definition."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _

from rest_framework import serializers

from data.services.utils import attach_email_icons
from data_appraisal.settings import FRONTEND_ROOT_URL

UserModel = get_user_model()


class CustomPasswordResetForm(PasswordResetForm):
    """Override class PasswordResetForm"""

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        use_https=False,
        token_generator=default_token_generator,
        request=None,
        html_email_template_name=None,
    ):
        """Override the send mail for reset password."""
        for user in self.get_users(self.cleaned_data["email"]):
            context = {
                "email": getattr(user, UserModel.get_email_field_name()),
                "domain": FRONTEND_ROOT_URL + "/Datapex",
                "site_name": get_current_site(request),
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token_generator.make_token(user),
                "user": user.first_name,
                "protocol": "https" if use_https else "http",
            }
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(template_name="password_reset_email.html", context=context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(body, "text/html")
        attach_email_icons(email_message, settings.IMAGES)
        email_message.send()


class PasswordResetSerializer(serializers.Serializer):
    """Serializer class for rest password model."""

    email = serializers.EmailField()
    password_reset_form_class = CustomPasswordResetForm

    def validate_email(self, value):
        """
        method to validate email.
        """
        self.reset_form = self.password_reset_form_class(  # pylint: disable=W0201
            data=self.initial_data
        )
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_("Error"))

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Invalid e-mail address"))
        return value

    def save(self):
        """override save method for serializer"""
        request = self.context.get("request")
        opts = {
            "use_https": request.is_secure(),
            "from_email": settings.DEFAULT_FROM_EMAIL,
            "email_template_name": "password_reset_email.html",
            "request": request,
        }
        self.reset_form.save(**opts)
