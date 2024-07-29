from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["email"] = self.user.email
        data["username"] = self.user.username
        data["name"] = self.user.first_name + " " + self.user.last_name
        data["role"] = self.user.role.name if self.user.role else None
        data["church"] = self.user.church.name if self.user.church else None
        data["birthdate"] = self.user.birthdate if self.user.birthdate else None
        data["phone"] = self.user.phone if self.user.phone else None

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
