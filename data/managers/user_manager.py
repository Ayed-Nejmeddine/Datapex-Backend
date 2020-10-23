from allauth.account.adapter import DefaultAccountAdapter
from data.models.user_model import Profile


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
            profile_data.update(country=data.get('country', False))
        if data.get('postalCode', False):
            profile_data.update(postalCode=data.get('postalCode', False))
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
        try:
            self.save_profile(user, data.get('profile'))
        except Exception:  # pylint: disable=W0703
            # delete just created user instance when exception is raised
            user.delete()
            return None
        user.save()
        return user