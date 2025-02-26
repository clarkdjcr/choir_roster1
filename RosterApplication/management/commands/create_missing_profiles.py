from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from RosterApplication.models import ChoirMember

class Command(BaseCommand):
    help = 'Creates missing ChoirMember profiles for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            try:
                user.choirmember
            except User.choirmember.RelatedObjectDoesNotExist:
                ChoirMember.objects.create(
                    user=user,
                    voice_part=None,
                    phone_number='',
                )
                self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}')) 