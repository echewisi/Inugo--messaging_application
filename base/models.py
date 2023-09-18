from django.db import models
from django.contrib.auth.models import User

class Profile(User):
    accesstoken= models.CharField(null= True, blank= True)
    refreshtoken= models.CharField(null=True, blank= True)
# Create your models here.
