from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import secrets


class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)
    confirmation_code_created = models.DateTimeField(default=timezone.now)

    def generate_confirmation_code(self):
        code = secrets.token_urlsafe(32)
        self.confirmation_code = code
        self.confirmation_code_created = timezone.now()
        self.save()
        return code

    def __str__(self):
        return self.username