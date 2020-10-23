from django.db.models.signals import post_init
from django.dispatch import receiver
from data.models.user_model import Profile
from phone_verify.models import SMSVerification


@receiver(post_init, sender=Profile)
def verify_phone(sender, instance, **kwargs):
    """verify phone number"""
    if instance.id:
        try:
            res = SMSVerification.objects.filter(phone_number=instance.phone).latest('created_at')
            instance.phone_is_verified = res.is_verified
        except SMSVerification.DoesNotExist:
            instance.phone_is_verified = False
        instance.save()
