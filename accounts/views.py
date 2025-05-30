from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import secrets
from .forms import RegistrationForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_confirmed = False
            confirmation_code = secrets.token_urlsafe(32)
            user.confirmation_code = confirmation_code
            user.save()

            # Отправка письма с кодом подтверждения
            subject = 'Подтверждение регистрации на MMORPG доске объявлений'
            message = f'Ваш код подтверждения: {confirmation_code}'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'На ваш email отправлен код подтверждения.')
            return redirect('confirm_email')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def confirm_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            user = User.objects.get(confirmation_code=code)
            user.email_confirmed = True
            user.confirmation_code = None
            user.save()
            login(request, user)
            return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'Неверный код подтверждения.')
    return render(request, 'accounts/confirm_email.html')