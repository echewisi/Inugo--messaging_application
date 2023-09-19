from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Profile(AbstractUser):
    name= models.CharField(max_length= 255, null= True, blank= False, default="anonymous")
    email= models.EmailField()
    bio= models.CharField(max_length= 255, null= True, blank= True)
    
    def __str__(self):
        return self.username
class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages', default= None)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering=['sent_at']

class Chat(models.Model):
    participants = models.ManyToManyField(Profile)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender= Profile)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.
