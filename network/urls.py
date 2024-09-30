
from django.urls import path

from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path('post/<int:id>', views.post, name="post"),
    path('follow/<int:id>', views.follow, name="follow"),
    path('unfollow/<int:id>', views.unfollow, name="unfollow"),
    path('edit/<int:id>', views.edit_post, name="edit"),
    path('like/<int:id>', views.like, name="like"),
    path('liked/<int:id>', views.liked, name="liked")
]


urlpatterns +=staticfiles_urlpatterns()