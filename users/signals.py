# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# To automatically create a new profile whenever a mew user is createdd and keep the profle synchronized

# As profile is created so no need for manual creation
@receiver(post_save, sender=User) #Connection with the function
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# TO save a profile, when they Profile model is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
