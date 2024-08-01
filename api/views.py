from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Role, Church, Event, Article, ArticleImage, EventImage, ArticleComment, EventComment, EventAttendee


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
        data["photo"] = self.user.photo.url if self.user.photo else None

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.get(email=request.GET.get('email'))
        user_details = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'birthdate': user.birthdate,
            'photo': request.build_absolute_uri(user.photo.url) if user.photo else None,
            'role': user.role.id if user.role else None,
            'church': user.church.id if user.church else None,
        }
        return Response(user_details, status=status.HTTP_200_OK)

class UserEditView(APIView):
    permission_classes = [IsAuthenticated]

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
    

class RoleView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        roles = Role.objects.all()
        roles_list = []
        for role in roles:
            roles_list.append({
                'id': role.id,
                'name': role.name,
            })
        return Response(roles_list, status=status.HTTP_200_OK)
    
class ChurchView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        churches = Church.objects.all()
        churches_list = []
        for church in churches:
            churches_list.append({
                'id': church.id,
                'name': church.name,
            })
        return Response(churches_list, status=status.HTTP_200_OK)
    
class EventView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        events = Event.objects.all()
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,
                'name': event.name,
                'description': event.description,
                'datetime': event.datetime,
                'location': event.location,
                'image': request.build_absolute_uri(EventImage.objects.filter(event=event).first().image.url) if EventImage.objects.filter(event=event).first() else None,
                'attendance': EventAttendee.objects.filter(event=event).count(),
            })
        return Response(events_list, status=status.HTTP_200_OK)
    
class EventDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        event = Event.objects.get(id=request.GET.get('id'))
        email = request.GET.get('email')

        event_details = {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'datetime': event.datetime,
            'location': event.location,
            'images': [request.build_absolute_uri(image.image.url) for image in EventImage.objects.filter(event=event)],
            'attendance': EventAttendee.objects.filter(event=event).count(),
            'comments': [{
                'content': comment.content,
                'datetime': comment.datetime,
                'author': comment.author.first_name + " " + comment.author.last_name,
                'photo': request.build_absolute_uri(comment.author.photo.url) if comment.author.photo else None,
            } for comment in EventComment.objects.filter(event=event)],
            'attending': EventAttendee.objects.filter(event=event, attendee=User.objects.get(email=email)).exists

        }
        return Response(event_details, status=status.HTTP_200_OK)

class EventAttendView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        event = Event.objects.get(id=data.get('event'))
        user = User.objects.get(email=data.get('email'))
        EventAttendee.objects.create(event=event, user=user)
        return Response(status=status.HTTP_200_OK)
    

class EventCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        event = Event.objects.get(id=data.get('event'))
        author = User.objects.filter(email=data.get('email')).first()
        EventComment.objects.create(event=event, author=author, content=data.get('content'))
        return Response(status=status.HTTP_200_OK)

class AttendEventView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        event = Event.objects.get(id=data.get('event'))
        user = User.objects.get(email=data.get('email'))
        EventAttendee.objects.create(event=event, attendee=user)
        return Response(status=status.HTTP_200_OK)
