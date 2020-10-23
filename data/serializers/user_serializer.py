from rest_auth.registration.serializers import RegisterSerializer as RootRegSerializer
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.serializers import UserDetailsSerializer
from data.models.user_model import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.
    """
    class Meta:  # pylint: disable=C0115
        model = Profile
        fields = ('id', 'phone', 'country', 'postalCode')


class RegisterSerializer(RootRegSerializer):  # pylint: disable=W0223
    """
    Gives custom serializer for user registration.
    """
    firstName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lastName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    profile = ProfileSerializer()


class UserSerializer(UserDetailsSerializer):
    """
    Add attributes in User detail serializer
    """

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        if hasattr(self.context.get("request"), 'user'):
            user = self.context.get("request").user
            self.fields['profile'] = ProfileSerializer()

    def update(self, instance, data):
        """Update both user and profile models."""
        profile = data.pop('profile')
        instance = super(UserSerializer, self).update(instance, data)
        if hasattr(instance, 'profile'):
            instance.profile.phone = profile['phone']
            instance.profile.country = profile['country']
            instance.profile.postalCode = profile['postalCode']
            instance.profile.save()
        return instance

    class Meta(UserDetailsSerializer.Meta):  # pylint: disable=C0115
        fields = UserDetailsSerializer.Meta.fields + ('profile', )
