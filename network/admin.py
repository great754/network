from django.contrib import admin
from network.models import User, Follow, Comment, Like, Post


# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)