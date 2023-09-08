from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"
    
    nickname = models.CharField(max_length=256, default='')
    image = models.ImageField(upload_to='', null=True)
