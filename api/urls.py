from django.urls import path
from . import views

urlpatterns = [
   path('register/', views.CreateUserView.as_view(), name='register'),
   path('edit/', views.UserEditView.as_view(), name='edit'),
   path('user/', views.UserView.as_view(), name='user'),
   path('roles/', views.RoleView.as_view(), name='roles'),
   path('churches/', views.ChurchView.as_view(), name='churches'),
   path('events/', views.EventView.as_view(), name='events'),
   path('event/', views.EventDetailView.as_view(), name='event'),
   path('event/attend/', views.EventAttendView.as_view(), name='event-attend'),
   path('event/comment/', views.EventCommentView.as_view(), name='event-comment'),
   path('event/attending/', views.AttendEventView.as_view(), name='attending'),
]
