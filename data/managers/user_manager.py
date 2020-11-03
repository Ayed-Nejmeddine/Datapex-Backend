from allauth.account.adapter import DefaultAccountAdapter
from data.models.user_model import Profile
from django.contrib.sites.shortcuts import get_current_site
from data_appraisal.settings import FRONTEND_ROOT_URL, ROOT_VERIFICATION, EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives


class RegisterAdapter(DefaultAccountAdapter):
    """This will represent a custom adapter for user registration."""

    def save_profile(self, user, data):
        """
        Save profile objects
        """
        profile_data = {}
        if data.get('phone', False):
            profile_data.update(phone=data.get('phone', False))
        if data.get('country', False):
            profile_data.update(country_id=data.get('country', False))
        if data.get('postalCode', False):
            profile_data.update(postalCode=data.get('postalCode', False))
        if data.get('company_name', False):
            profile_data.update(company_name=data.get('company_name', False))
        if data.get('photo', False):
            profile_data.update(photo=data.get('photo', False))
        if data.get('occupation', False):
            profile_data.update(occupation=data.get('occupation', False))
        if data.get('language', False):
            profile_data.update(language=data.get('language', False))
        if data.get('city', False):
            profile_data.update(city_id=data.get('city', False))
        profile_obj = Profile.objects.update_or_create(user=user, defaults=profile_data)
        return profile_obj

    def save_user(self, request, user, form, commit=True):  # pylint: disable=W0613
        """
        Overriding this method to update the corresponding profile of a specific user.
        """
        user = super(RegisterAdapter, self).save_user(request, user, form, commit=True)
        data = form.data
        # update user model
        if data.get('firstName', False):
            user.first_name = data.get('firstName')
        if data.get('lastName', False):
            user.last_name = data.get('lastName')
        # create profile
        user.save()
        try:
            self.save_profile(user, data.get('profile'))
        except Exception:  # pylint: disable=W0703
            # delete just created user instance when exception is raised
            user.delete()
            return None
        return user

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """ Override the send confirmation mail method. """
        site = get_current_site(request)
        link = FRONTEND_ROOT_URL + ROOT_VERIFICATION + '?token=' + emailconfirmation.key
        ctx = {
            "username": emailconfirmation.email_address.user.username,
            "site": site,
            "link": link,
        }
        html_content = render_to_string(template_name="confirm_email.html",
                                        context=ctx)
        msg = EmailMultiAlternatives(_("Please confirm your email"), html_content,
                                     EMAIL_HOST_USER, [emailconfirmation.email_address])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
