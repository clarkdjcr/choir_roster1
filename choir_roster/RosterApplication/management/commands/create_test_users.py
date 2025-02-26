from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from RosterApplication.models import ChoirMember

class Command(BaseCommand):
    help = 'Creates test users and choir members'

    def handle(self, *args, **kwargs):
        # Create test users
        test_users = [
            ('john', 'John', 'Doe', 'S1'),
            ('jane', 'Jane', 'Smith', 'A1'),
            ('bob', 'Bob', 'Wilson', 'T1'),
        ]

        for username, first, last, voice_part in test_users:
            user = User.objects.create_user(
                username=username,
                password='testpass123',
                first_name=first,
                last_name=last,
                email=f'{username}@example.com'
            )
            
            ChoirMember.objects.create(
                user=user,
                voice_part=voice_part,
                folder_number=None,
                phone_number='',
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created user {username}')) 