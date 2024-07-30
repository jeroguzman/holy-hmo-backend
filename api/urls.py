from django.urls import path
from . import views

urlpatterns = [
   path('register/', views.CreateUserView.as_view(), name='register'),
   path('edit/', views.UserEditView.as_view(), name='edit'),
]
