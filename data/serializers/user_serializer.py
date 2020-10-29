from rest_auth.registration.serializers import RegisterSerializer as RootRegSerializer
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.serializers import UserDetailsSerializer
from data.models.user_model import Profile
from phonenumber_field import phonenumber
from django_countries import Countries


class SerializableCountryField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super(SerializableCountryField, self).__init__(choices=Countries(), default=None)

    def to_representation(self, value):
        if value in ('', None):
            return None # normally here it would return value. which is Country(u'') and not serialiable
        return super(SerializableCountryField, self).to_representation(value)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.
    """
    country = SerializableCountryField(allow_null=True, required=False, allow_blank=True)
    phone_is_verified = serializers.ReadOnlyField()
    def validate_phone(self, phone):
        """
         Validate phone number field
        """
        user = self.context.get("request").user
        if self.context.get('request').method == 'PUT':
            phone_count = Profile.objects.filter(user=user, phone=phone).count()
            if phone_count != 1:
                # new phone number
                phone_count = Profile.objects.filter(phone=phone).count()
                if phone_count:
                    raise serializers.ValidationError("Invalid phone number!")
        if self.context.get('request').method == 'POST':
            phone_count = Profile.objects.filter(phone=phone).count()
            if phone_count:
                raise serializers.ValidationError("Phone number is already in use!")

        phone_number = phonenumber.to_python(phone)  # pylint: disable = W0642
        if phone_number and not phone_number.is_valid():
            raise serializers.ValidationError("Invalid phone number!")
        return phone

    class Meta:  # pylint: disable=C0115
        model = Profile
        fields = ('id', 'phone', 'postalCode', 'country', 'company_name', 'phone_is_verified','photo')


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
            instance.profile.company_name = profile['company_name']
            instance.profile.photo = profile['photo']
            instance.profile.save()
        return instance

    class Meta(UserDetailsSerializer.Meta):  # pylint: disable=C0115
        fields = UserDetailsSerializer.Meta.fields + ('profile', )
