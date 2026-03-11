import os
from django.core.management.base import BaseCommand, CommandError
from accounts.models import User

class Command(BaseCommand):
    help = 'Seeds the initial admin user'

    def handle(self, *args, **options):
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        if not admin_email or not admin_password:
            raise CommandError('ADMIN_EMAIL and ADMIN_PASSWORD environment variables must be set.')
        
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                name='Super Admin',
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {admin_email}'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user {admin_email} already exists.'))
