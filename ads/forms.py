from django import forms
from .models import Advertisement, Response, Category
from django.core.exceptions import ValidationError


class AdvertisementForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию",
        label="Категория"
    )

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category']  # Добавьте другие поля по необходимости
        widgets = {
            'content': forms.Textarea(attrs={'class': 'django_ckeditor_5'}),
        }

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if video.size > 50 * 1024 * 1024:  # 50MB
                raise ValidationError("Видео слишком большое (макс. 50MB)")
            if not video.name.lower().endswith(('.mp4', '.mov', '.avi')):
                raise ValidationError("Поддерживаются только MP4, MOV и AVI форматы")
        return video


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }