from django.contrib import admin
from .models import Category, Asset, Broker, Review, Newsletter

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title') # Що показувати у списку

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'ticker', 'api_ticker', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('title', 'ticker', 'api_ticker')

@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('title', 'website', 'created_at', 'updated_at')
# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Відображаємо ключові поля у списку
    list_display = ('asset', 'author', 'rating', 'is_approved', 'created_at')
    
    # Додаємо фільтри збоку (дуже зручно фільтрувати "Неодобрені")
    list_filter = ('is_approved', 'rating', 'asset')
    
    # Робимо поле is_approved редагованим прямо зі списку (щоб не заходити в кожен відгук окремо)
    list_editable = ('is_approved',)
    
    # Додаємо пошук по тексту відгуку або імені автора
    search_fields = ('author', 'text')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    # Виводимо email та дату підписки
    list_display = ('email', 'subscribed_at')
    
    # Додаємо можливість пошуку за email
    search_fields = ('email',)
    
    # Сортуємо: спочатку найновіші підписки
    ordering = ('-subscribed_at',)
from .models import SubscriptionPlan, Order

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'created_at')