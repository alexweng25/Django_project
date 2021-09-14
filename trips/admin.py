from django.contrib import admin

# Register your models here.
from .models import Photos, Post

admin.site.register(Post)
admin.site.register(Photos)
