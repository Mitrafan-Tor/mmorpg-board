from django import forms
from .models import Advertisement, Response, Category
from django.core.exceptions import ValidationError


class AdvertisementForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    video = forms.FileField(required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию",
        label="Категория"
    )
    clear_image = forms.BooleanField(required=False, label="Удалить текущее изображение")
    clear_video = forms.BooleanField(required=False, label="Удалить текущее видео")

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'django_ckeditor_5'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'accept': 'video/*'}),
        }

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if video.size > 50 * 1024 * 1024:  # 50MB
                raise ValidationError("Видео слишком большое (макс. 50MB)")
            if not video.name.lower().endswith(('.mp4', '.mov', '.avi')):
                raise ValidationError("Поддерживаются только MP4, MOV и AVI форматы")
        return video

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:  # 5MB
            raise ValidationError("Изображение слишком большое (максимум 5MB)")
        return image


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }