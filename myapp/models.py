from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.contrib.auth.models import User
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

    
class blog(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    blog_image = models.ImageField(upload_to="blogPic")
    category= models.CharField(max_length=150, blank=True,null=True)
    summary = models.CharField( max_length=150, blank=True,null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True,db_constraint=False)
    Content = models.TextField(blank=True,null=True)
    is_draft = models.BooleanField(default=False)

    
class appointment(models.Model):
    user = models.CharField(max_length=50)
    doctor = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    speciality = models.CharField(max_length=50)
    date = models.DateField()
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    
