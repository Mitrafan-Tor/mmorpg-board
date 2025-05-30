from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Advertisement, Response, Category
from .forms import AdvertisementForm, ResponseForm
from accounts.models import User


@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('advertisement_detail', pk=ad.pk)
    else:
        form = AdvertisementForm()
    return render(request, 'ads/create_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk, author=request.user)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('advertisement_detail', pk=ad.pk)
    else:
        form = AdvertisementForm(instance=ad)
    return render(request, 'ads/edit_advertisement.html', {'form': form})


def advertisement_detail(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = ad
            response.author = request.user
            response.save()

            # Отправка уведомления автору объявления
            subject = f'Новый отклик на ваше объявление "{ad.title}"'
            message = f'Пользователь {request.user.username} оставил отклик на ваше объявление "{ad.title}":\n\n{response.text}'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [ad.author.email],
                fail_silently=False,
            )

            messages.success(request, 'Ваш отклик успешно отправлен!')
            return redirect('advertisement_detail', pk=ad.pk)
    else:
        form = ResponseForm()

    responses = ad.response_set.all()
    return render(request, 'ads/advertisement_detail.html', {
        'ad': ad,
        'form': form,
        'responses': responses,
    })


@login_required
def my_responses(request):
    my_ads = Advertisement.objects.filter(author=request.user)
    responses = Response.objects.filter(advertisement__in=my_ads)

    # Фильтрация по объявлению
    ad_filter = request.GET.get('ad_filter')
    if ad_filter:
        responses = responses.filter(advertisement_id=ad_filter)

    return render(request, 'ads/my_responses.html', {
        'responses': responses,
        'my_ads': my_ads,
    })


@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk, advertisement__author=request.user)
    response.accepted = True
    response.save()

    # Отправка уведомления автору отклика
    subject = f'Ваш отклик на объявление "{response.advertisement.title}" принят!'
    message = f'Автор объявления "{response.advertisement.title}" принял ваш отклик.'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [response.author.email],
        fail_silently=False,
    )

    messages.success(request, 'Отклик принят! Автор уведомлен.')
    return redirect('my_responses')


@login_required
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk, advertisement__author=request.user)
    response.delete()
    messages.success(request, 'Отклик удален.')
    return redirect('my_responses')

def home(request):
    categories = Category.objects.all()
    advertisements = Advertisement.objects.all().order_by('-created_at')
    return render(request, 'ads/home.html', {
        'categories': categories,
        'advertisements': advertisements,
    })