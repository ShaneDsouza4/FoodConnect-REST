from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import UpdateProfileSerializer
from rest_framework.generics import UpdateAPIView
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# User Registration Vieww
class RegisterView(APIView):
    permission_classes = [AllowAny] # To allow users to access the Register APIs, without authentication usssue

    def post(self, request):

        serializer = RegisterSerializer(data=request.data) # Intialized the serializer with the request object

        # Verify is the request obj valid
        if serializer.is_valid():
            user = serializer.save() # Save the user
            refresh = RefreshToken.for_user(user) #Gernerate the JWT tokens

            # In return will send back the JWT refresh and access token in the respone object
            return Response({
                "message": "User registered successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        #Incase data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for logging in
class LoginView(APIView):

    permission_classes = [AllowAny]  # Allow all users to access the login

    def post(self, request):

        #Extract thee email and passwordd
        email = request.data.get('email')
        password = request.data.get('password')

        # Finding the user by the email provided
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        # By default Django requuires username and password to authenticate
        user = authenticate(username=user.username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user) #JWT Token
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


# Logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated] #Only authenticated users can access

    def post(self, request):
        try:
            # Will extract the refresh token from the req body
            refresh_token = request.data.get("refresh")

            #Check if the user provided
            if not refresh_token:
                return Response({"error": "Refresh token is missing"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist process to logout the user
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(f"Logout error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Updating the user profile
class UpdateProfileView(UpdateAPIView):
    # Query set and sequlizer class
    queryset = Profile.objects.all()
    serializer_class = UpdateProfileSerializer

    #Only authenticated user can access
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile # Return the profile


# Details view
class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated] #Only authenticated users

    def get(self, request):
        try:
            profile = request.user.profile  # Profile of the loggedin user
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)