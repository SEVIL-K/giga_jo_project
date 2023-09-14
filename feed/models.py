from django.db import models
from user.models import UserModel

# Create your models here.


class Feed(models.Model):
    class Meta:
        db_table = "feed"

    # user값이 들어온다면 null을 지워줘야함
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    title = models.CharField(max_length=256, default='')
    image = models.ImageField(upload_to='', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)


class FeedComment(models.Model):
    class Meta:
        db_table = "comment"

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE) # 작성자
    content = models.TextField(max_length=256) # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content
