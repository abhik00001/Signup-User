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
    
class blog(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    blog_image = models.ImageField(upload_to="blogPic")
    category= models.CharField(max_length=150, blank=True,null=True)
    summary = models.CharField( max_length=150, blank=True,null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Content = models.TextField(blank=True,null=True)
    is_draft = models.BooleanField(default=False)

    

    
