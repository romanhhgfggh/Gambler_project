from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")

    def __str__(self):
        return self.title

class Asset(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва активу")
    ticker = models.CharField(max_length=10, verbose_name="Тікер (символ)")
    api_ticker = models.CharField(max_length=20, verbose_name="Тікер для API", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='assets', verbose_name="Категорія")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Поточна ціна")
    
    description = models.TextField(blank=True, null=True, verbose_name="Опис активу")
    image = models.ImageField(upload_to='assets_images/', blank=True, null=True, verbose_name="Логотип")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return f"{self.title} ({self.ticker})"

class Broker(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва брокера")
    website = models.URLField(verbose_name="Сайт")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.title
class Review(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='reviews', verbose_name="Актив")
    author = models.CharField(max_length=100, verbose_name="Ваше ім'я", default="Анонімний трейдер")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оцінка (1-5)")
    text = models.TextField(verbose_name="Відгук")
    
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.title} - {self.rating}/5"

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email для розсилки")
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
# Create your models here.
