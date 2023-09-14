from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from feed.models import Feed

# Create your models here.


class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    nickname = models.CharField(max_length=256, default='')
    image = models.ImageField(upload_to='', blank=True, null=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    liked_feed = models.ManyToManyField("feed.Feed", default=None, null=True)