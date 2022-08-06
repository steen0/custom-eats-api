from django.core.management.base import BaseCommand, CommandError

from core.models import User


class Command(BaseCommand):
    help = 'Upgrades users to superusers.'

    def add_arguments(self, parser):
        parser.add_argument('user_email', nargs='+')

    def handle(self, *args, **options):
        try:
            user_email = options['user_email'][0]
            user = User.objects.get(email = user_email)
        except User.DoesNotExist:
            raise CommandError('\nUser %s does not exist' % user_email)

        if user.is_superuser:
            self.stdout.write(self.style.WARNING(
                '\nUser %s is already a superuser' % user_email
                ))
        else:
            User.objects.upgrade_user(email=user_email)
            self.stdout.write(self.style.SUCCESS(
                '\nSuccessfully upgraded user %s' % user_email
                ))
