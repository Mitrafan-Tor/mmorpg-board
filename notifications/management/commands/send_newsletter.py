from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from accounts.models import User
from mmorpg_board import settings


class Command(BaseCommand):
    help = 'Send newsletter to all users'

    def add_arguments(self, parser):
        parser.add_argument('subject', type=str)
        parser.add_argument('message', type=str)

    def handle(self, *args, **options):
        users = User.objects.filter(email_confirmed=True)
        subject = options['subject']
        message = options['message']

        emails = [
            (subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            for user in users
        ]

        send_mass_mail(emails)
        self.stdout.write(self.style.SUCCESS(f'Successfully sent {len(emails)} emails'))