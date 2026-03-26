from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")

    def __str__(self):
        return self.title

class Asset(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва активу")
    ticker = models.CharField(max_length=10, verbose_name="Тікер (символ)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='assets', verbose_name="Категорія")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Поточна ціна")
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
# Create your models here.
