from django.db import models
from django.contrib.auth.models import User
import os


class Account(models.Model):

    user = models.OneToOneField(User,null = True,on_delete= models.CASCADE)

    follow = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    profile_pic = models.ImageField(upload_to='profiles_pics/', default=None, null=True, blank=True)

    google_scholar = models.URLField(max_length=200,null=True,blank=True)
    linkedin = models.URLField(max_length=200,null=True,blank=True)
    github = models.URLField(max_length=200,null=True,blank=True)
    website = models.URLField(max_length=200,null=True,blank=True)

    new_notifications = models.BooleanField(default = False)

    def __str__(self):
        return str(self.user.last_name) + ' ' + str(self.user.first_name)

    def profile_pic_image_url(self):
        if profile_pic is None:
            return 

class AllowedEmail(models.Model):
    email = models.EmailField(null=True,blank=False)
    def __str__(self):
        return str(self.email)