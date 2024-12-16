from django.db import models

from django.contrib.auth.models import AbstractUser

#---------------------------------------------------

class User(AbstractUser):
    '''
    A custom user with a unique email inherited from AbstractUser
    '''
    first_name = models.CharField(max_length=15,blank=True)
    last_name = models.CharField(max_length=20,blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=90)
    username = None
    # tfa_secret = models.CharField(max_length=255, default='')    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

class UserToken(models.Model):
    '''
    A model for managing token authentication for users
    '''
    user_id = models.IntegerField()
    token = models.CharField(max_length=500)
    create = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField()
     

class Reset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=500 , unique=True)
    