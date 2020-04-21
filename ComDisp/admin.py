from django.contrib import admin
from .models import Comment, videoInfo

admin.site.register(Comment)
admin.site.register(videoInfo)