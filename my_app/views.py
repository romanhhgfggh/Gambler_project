from django.shortcuts import render, get_object_or_404
from .models import Asset, Category

def home(request, cat_id=None):
    categories = Category.objects.all()
    
    if cat_id:
        assets = Asset.objects.filter(category_id=cat_id)
        current_category = Category.objects.get(id=cat_id)
        title = f"Категорія: {current_category.title}"
    else:
        assets = Asset.objects.all()
        title = "Всі активи"

    context = {
        'assets': assets,
        'categories': categories,
        'title': title,
    }
    return render(request, 'pages/index.html', context)
def about(request):
    categories = Category.objects.all() 
    return render(request, 'pages/about.html', {'categories': categories})

def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    categories = Category.objects.all()
    
    context = {
        'asset': asset,
        'categories': categories,
        'title': asset.title,
    }
    return render(request, 'pages/asset_detail.html', context)