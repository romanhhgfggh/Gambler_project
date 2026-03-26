from django.contrib import admin
from .models import Category, Asset, Broker

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title') # Що показувати у списку

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    # Відображаємо назву, дату створення та оновлення, як просив викладач
    list_display = ('title', 'category', 'price', 'created_at', 'updated_at')
    list_filter = ('category',) # Додаємо фільтр збоку
    search_fields = ('title', 'ticker') # Додаємо пошук

@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('title', 'website', 'created_at', 'updated_at')
# Register your models here.
