"""
    This serializer represent the serializer of the user.
    """

from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from cities_light.models import City
from cities_light.models import Country
from django_countries import Countries
from phonenumber_field import phonenumber
from rest_auth.registration.serializers import RegisterSerializer as RootRegSerializer
from rest_auth.serializers import LoginSerializer
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from data.models.user_model import Profile
from data.services.utils import send_email


class SerializableCountryField(serializers.ChoiceField):  # pylint: disable=R0903
    """country serializer"""

    def __init__(self, **kwargs):
        super().__init__(choices=Countries(), default=None)

    def to_representation(self, value):
        """representation"""
        if value in ("", None):
            return None  # normally here it would return value. which is Country(u'') and not serialiable
        return super().to_representation(value)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.
    """

    country = serializers.CharField()
    phone_is_verified = serializers.ReadOnlyField()
    email_is_verified = serializers.ReadOnlyField()
    city = serializers.CharField()

    def validate_city(self, city):
        """validate city by name"""
        city = City.objects.filter(name=city).first()
        if not city:
            raise serializers.ValidationError("city not found!")
        return city.id

    def validate_country(self, country):
        """validate country by name"""
        country = Country.objects.filter(name=country).first()
        if not country:
            raise serializers.ValidationError("country not found!")
        return country.id

    def validate_phone(self, phone):
        """
        Validate phone number field
        """
        user = self.context.get("request").user
        if self.context.get("request").method == "PUT":
            phone_count = Profile.objects.filter(user=user, phone=phone).count()
            if phone_count != 1:
                # new phone number
                phone_count = Profile.objects.filter(phone=phone).count()
                if phone_count:
                    raise serializers.ValidationError("Invalid phone number!")
        if self.context.get("request").method == "POST":
            phone_count = Profile.objects.filter(phone=phone).count()
            if phone_count:
                raise serializers.ValidationError("Phone number is already in use!")

        phone_number = phonenumber.to_python(phone)  # pylint: disable = W0642
        if phone_number and not phone_number.is_valid():
            raise serializers.ValidationError("Invalid phone number!")
        return phone

    class Meta:  # pylint: disable=C0115,R0903
        model = Profile
        fields = (
            "id",
            "phone",
            "postalCode",
            "country",
            "city",
            "company",
            "occupation",
            "phone_is_verified",
            "email_is_verified",
            "photo",
            "language",
            "gender",
        )


class RegisterSerializer(RootRegSerializer):  # pylint: disable=W0223,R0903
    """
    Gives custom serializer for user registration.
    """

    firstName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lastName = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    profile = ProfileSerializer()

    def save(self, request):
        """Override of save funtion in register serializer"""
        user = super().save(request)
        ctx = {
            "username": user,
            "email": user.email,
        }
        send_email("confirm_inscription.html", "Your registration is confirmed", ctx, user)
        return user


class UserSerializer(UserDetailsSerializer):  # pylint: disable=R0903
    """
    Add attributes in User detail serializer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.context.get("request"), "user"):
            self.fields["profile"] = ProfileSerializer()

    def validate_email(self, value):
        """
        Check if the email is unique.
        """
        user = self.context["request"].user

        # Check if the email is being updated and if the new email is different from the current one
        if user.email != value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user is already registered with this e-mail address."
            )
        return value

    def update(self, instance, data):
        """Update both user and profile models."""
        profile = data.pop("profile")
        email = data.get("email", None)
        instance = super().update(instance, data)
        if email and not EmailAddress.objects.filter(email=email):
            EmailAddress.objects.get(user_id=instance.id).delete()
            EmailAddress.objects.create(
                email=email, primary=True, verified=False, user_id=instance.id
            )

        if hasattr(instance, "profile"):
            if profile.get("phone", False):
                instance.profile.phone = profile["phone"]
            if profile.get("country", False):
                country = Country.objects.filter(id=profile["country"]).first()
                # pylint: disable=W0212
                instance.profile._country = country
            if profile.get("city", False):
                city = City.objects.filter(id=profile["city"]).first()
                # pylint: disable=W0212
                instance.profile._city = city
            if profile.get("postalCode", False):
                instance.profile.postalCode = profile["postalCode"]
            if profile.get("company", False):
                instance.profile.company = profile["company"]
            if profile.get("photo", False):
                instance.profile.photo = profile["photo"]
            if profile.get("occupation", False):
                instance.profile.occupation = profile["occupation"]
            if profile.get("language", False):
                instance.profile.language = profile["language"]
            if profile.get("gender", False):
                instance.profile.gender = profile["gender"]
            instance.profile.save()
        return instance

    class Meta(UserDetailsSerializer.Meta):  # pylint: disable=C0115,R0903
        fields = UserDetailsSerializer.Meta.fields + ("profile",)
        read_only_fields = tuple(
            field for field in UserDetailsSerializer.Meta.read_only_fields if field != "email"
        )


class UploadPhotoSerializer(serializers.ModelSerializer):  # pylint: disable=R0903
    """
    Serializer for Upload Profile photo.
    """

    photo = serializers.ImageField(required=True)

    class Meta:  # pylint: disable=R0903
        """Meta class"""

        model = Profile
        fields = ("photo",)


class UserLoginSerializer(LoginSerializer):  # pylint: disable=R0903
    """
    Serializer for Login
    """

    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)
