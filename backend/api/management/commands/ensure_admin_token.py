from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class Command(BaseCommand):
    help = 'Ensures a default admin user exists and generates a JWT token'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'
        
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
        else:
            self.stdout.write(f'User {username} already exists')

        refresh = RefreshToken.for_user(user)
        self.stdout.write(self.style.SUCCESS(f'JWT Access Token (valid for 24h): {str(refresh.access_token)}'))

