from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from booking.models import Currency


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if Currency.objects.count() > 0:
            Profile.objects.create(user=instance, default_currency = Currency.objects.first())
            return
        Profile.objects.create(user=instance)



