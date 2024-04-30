from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
# Create your models here.

        
class CustomUser(AbstractUser,PermissionsMixin):
    user_type = models.CharField(max_length=150,default="patient", blank=True)
    profile_pic = models.ImageField(upload_to="profilepic/", blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField( max_length=50, blank=True)
    state = models.CharField( max_length=50, blank=True)
    pincode = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.username
