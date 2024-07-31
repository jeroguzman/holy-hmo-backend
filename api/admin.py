from django.contrib import admin
from .models import User, Church, Role, Event, Article, ArticleImage, EventImage, ArticleComment, EventComment, EventAttendee

admin.site.register(User)
admin.site.register(Church)
admin.site.register(Role)
admin.site.register(Event)
admin.site.register(Article)
admin.site.register(ArticleImage)
admin.site.register(EventImage)
admin.site.register(ArticleComment)
admin.site.register(EventComment)
admin.site.register(EventAttendee)

# Register your models here.
