from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Generate a token for a user'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username= "joseph")
            token, created = Token.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Token created for {user.username}: {token.key}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Superuser not found'))
