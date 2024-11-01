from django.db import models
from django.contrib.auth.models import User

# Profile modes to strore additional user details, linking to Django User model

class Profile(models.Model):
    # Roles for the user to select from the dropdown
    USER_ROLES = [
        ('superadmin', 'Superadmin'),
        ('individual', 'Individual'),
        ('foodbank', 'Foodbank'),
        ('restaurant', 'Restaurant'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE) # one to one with the builtin User model
    role = models.CharField(max_length=20, choices=USER_ROLES)
    id_card_image = models.CharField(max_length=500, null=True, blank=True) # Will be S3 url
    verified = models.BooleanField(default=False)  # We will review image and verify the user

    def __str__(self):
        return f"{self.user.username} - {self.role}"