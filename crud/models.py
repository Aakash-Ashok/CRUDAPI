from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserManage(AbstractUser):
    email = models.EmailField(unique=True)

  

class BookModel(models.Model):
    user=models.ForeignKey(UserManage,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    price=models.IntegerField()
    
    
    
    
