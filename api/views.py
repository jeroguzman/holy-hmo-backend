from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Role, Church


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

class UserEditView(APIView):
    def put(self, request):
        data = request.data
        user = User.objects.get(email=data.get('email'))
        
        if 'username' in data:
            user.username = data.get('username')
        if 'email' in data:
            user.email = data.get('email')
        if 'first_name' in data:
            user.first_name = data.get('first_name')
        if 'last_name' in data:
            user.last_name = data.get('last_name')
        if 'phone' in data:
            user.phone = data.get('phone')
        if 'birthdate' in data:
            user.birthdate = data.get('birthdate')
        if 'photo' in data:
            user.photo = request.FILES.get('photo')
        if 'role' in data:
            user.role = Role.objects.get(id=data.get('role'))
        if 'church' in data:
            user.church = Church.objects.get(id=data.get('church'))
       
        user.save()

        return Response(status=status.HTTP_200_OK)
    

def update_profile(request, id):
    user = User.objects.get(id=id)
    data = request.data

    user.name = data.get('name')
    user.email = data.get('email')
    user.photo = request.FILES.get('photo') if request.FILES.get('photo') else None
    user.phone_no = data.get('phone_no')
    user.allow_wa = True if data.get('allow_wa') == 'true' else False
    user.allow_calls = True if data.get('allow_calls') == 'true' else False

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
