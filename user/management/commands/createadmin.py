from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create superuser"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from user.models import User

        superuser_username = settings.SUPERUSER_USERNAME
        superuser_email = settings.SUPERUSER_EMAIL
        superuser_password = settings.SUPERUSER_PASSWORD

        if not User.objects.filter(username=superuser_username).exists():
            User.objects.create_superuser(superuser_username, superuser_email, superuser_password)

        self.stdout.write(self.style.SUCCESS("Successfully created superuser"))

