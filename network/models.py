from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date, datetime

class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    likes = models.IntegerField(default=0)
    post_date = models.DateField(default=date.today())
    time = models.TimeField(default=datetime.now().time())

    def __str__(self):
        return f"{self.poster} posted {self.content} with {self.likes} likes on {self.post_date} at {self.time}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.liker} liked {self.post}"

class Follow(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.user1} followed {self.user2}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.TimeField(default=datetime.now().time())
    comment_date = models.DateField(default=date.today())
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    entry = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.commenter} commented {self.entry} on {self.post}"