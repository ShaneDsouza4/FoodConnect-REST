# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
import random

# WIll contain serializers to convert into a JSON Object

# Register new user
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Won't be included in the output
    role = serializers.ChoiceField(choices=Profile.USER_ROLES)
    id_card_image = serializers.CharField(write_only=True) # Stored at S3 bucket. Won't be in response

    class Meta:
        # Link serializer to user modell
        model = User

        # Fields to use
        fields = ['first_name', 'last_name', 'email', 'password', 'role', 'id_card_image']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
        }

    # Check if the email exists in the DB
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    # Create the new user
    def create(self, validated_data):

        # Extract role and image from the valid data
        role = validated_data.pop('role')
        id_card_image = validated_data.pop('id_card_image')

        # Generate a username, as not asking to enter username
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        generated_username = f"{first_name}{last_name}{random.randint(1000, 9999)}"

        # Username is now added
        user = User.objects.create_user(
            username=generated_username,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )

        # Linked to the Profile instance
        Profile.objects.create(user=user, role=role, id_card_image=id_card_image)

        # Created user is sent
        return user

# Updating existing user profile
class UpdateProfileSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.USER_ROLES, required=False)
    id_card_image = serializers.CharField(required=False)  # Updated to CharField for S3 URL

    class Meta:
        # Link serializer to the Profile model
        model = Profile

        #Fields to use
        fields = ['role', 'id_card_image', 'verified']
        read_only_fields = ['verified'] #User cannot modify

# View user information
class ProfileSerializer(serializers.ModelSerializer):
    # Get user name, and email from the User Model
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        # Linked the serializer to the Profile model and fields to use
        model = Profile
        fields = ['username', 'email', 'role', 'id_card_image', 'verified']
