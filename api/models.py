from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Church(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Role(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    datetime = models.DateTimeField()
    location = models.CharField(max_length=100)
        
    def __str__(self):
        return self.name
        
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.title
        
class ArticleImage(models.Model):
    image = models.ImageField(upload_to='media/')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.image.url
    
class EventImage(models.Model):
    image = models.ImageField(upload_to='media/')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.image.url
    
class ArticleComment(models.Model):
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.content

class EventComment(models.Model):
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.content
    
class EventAttendee(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.attendee.username