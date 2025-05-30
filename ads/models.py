from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Tanks', 'Танки'),
        ('Heals', 'Хилы'),
        ('DD', 'ДД'),
        ('Merchants', 'Торговцы'),
        ('Guildmasters', 'Гилдмастеры'),
        ('Questgivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Tanners', 'Кожевники'),
        ('Potionmakers', 'Зельевары'),
        ('Spellmasters', 'Мастера заклинаний'),
    ]

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Advertisement(models.Model):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(5)])
    content = CKEditor5Field('Text', config_name='default')
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True, verbose_name="Изображение")
    video = models.FileField(upload_to='ads_videos/', blank=True, null=True, verbose_name="Видео")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(validators=[MinLengthValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Response to {self.advertisement.title} by {self.author.username}"