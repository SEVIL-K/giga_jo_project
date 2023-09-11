from django.db import models
from user.models import UserModel

# Create your models here.


class Feed(models.Model):
    class Meta:
        db_table = "feed"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    title = models.CharField(max_length=256, default='')
    image = models.ImageField(upload_to='', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedComment(models.Model):
    class Meta:
        db_table = "comment"

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
