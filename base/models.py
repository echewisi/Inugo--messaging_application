from django.db import models
from django.contrib.auth.models import User

class Profile(User):
    accesstoken= models.CharField(null= True, blank= True)
    refreshtoken= models.CharField(null=True, blank= True)



class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

# Create your models here.
