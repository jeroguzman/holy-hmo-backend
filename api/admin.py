from django.contrib import admin
from .models import User, Church, Role

admin.site.register(User)
admin.site.register(Church)
admin.site.register(Role)

# Register your models here.
