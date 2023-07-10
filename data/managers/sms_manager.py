"""Define SMS Manager"""
from phone_verify.backends.twilio import TwilioBackend
from phone_verify.models import SMSVerification
from django.conf import settings
import jwt
import random


class CustomTwilioBackend(TwilioBackend):
    """Override Twilio backend in order to disable deleting SmsVerification objects"""

    def create_security_code_and_session_token(self, number):
        """
        Creates a temporary `security_code` and `session_token` inside the DB.

        `security_code` is the code that user would enter to verify their phone_number.
        `session_token` is used to verify if the subsequent call for verification is
        by the same device that initiated a phone number verification in the
        first place.

        :param number: Phone number of recipient

        :return security_code: string of sha security_code
        :return session_token: string of session_token
        """
        security_code = self.generate_security_code()
        data = {"phone_number": number, "nonce": random.random(),"security_code":security_code}
        session_token= jwt.encode(data, settings.SECRET_KEY)
        # Default security_code generated of 6 digits
        SMSVerification.objects.create(
            phone_number=number,
            security_code=security_code,
            session_token=session_token,
        )
        return security_code, session_token
