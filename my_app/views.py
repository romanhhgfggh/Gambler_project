from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Asset, Category, Broker
from .forms import ReviewForm, NewsletterForm
import yfinance as yf

def home(request):
    assets = Asset.objects.all()
    categories = Category.objects.all()
    for asset in assets:
        target_ticker = asset.api_ticker if asset.api_ticker else asset.ticker
        if target_ticker:
            try:
                yf_asset = yf.Ticker(target_ticker)
                asset.dynamic_price = round(yf_asset.fast_info['lastPrice'], 4)
            except Exception:
                asset.dynamic_price = asset.price
        else:
            asset.dynamic_price = asset.price

    context = {
        'assets': assets,
        'categories': categories,
    }
    return render(request, 'pages/index.html', context)

def about(request):
    categories = Category.objects.all() 
    return render(request, 'pages/about.html', {'categories': categories})

def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    categories = Category.objects.all()
    reviews = asset.reviews.filter(is_approved=True)
    brokers = Broker.objects.all()
    
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    reviewed_assets = request.session.get('reviewed_assets', [])
    has_reviewed = asset.id in reviewed_assets

    dynamic_price = asset.price 
    
    target_ticker = asset.api_ticker if asset.api_ticker else asset.ticker
    try:
        if target_ticker:
            yf_asset = yf.Ticker(target_ticker)
            dynamic_price = round(yf_asset.fast_info['lastPrice'], 4)
    except Exception as e:
        print(f"Помилка API для {target_ticker}: {e}")

    if request.method == 'POST' and 'submit_review' in request.POST:
        if not has_reviewed:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.asset = asset
                review.save()
                reviewed_assets.append(asset.id)
                request.session['reviewed_assets'] = reviewed_assets
                return redirect('assets_detailed', asset_id=asset.id)
    else:
        review_form = ReviewForm()
    context = {
        'asset': asset,
        'categories': categories,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else "Немає оцінок",
        'review_form': review_form,
        'brokers': brokers,
        'has_reviewed': has_reviewed,
        'dynamic_price': dynamic_price
    }
    return render(request, 'pages/asset_detail.html', context)

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('home')

def add_to_watchlist(request, asset_id):
    watchlist = request.session.get('watchlist', [])
    if asset_id not in watchlist:
        watchlist.append(asset_id)
    request.session['watchlist'] = watchlist
    return redirect('watchlist_view')

def watchlist_view(request):
    categories = Category.objects.all()
    watchlist_ids = request.session.get('watchlist', [])
    assets = Asset.objects.filter(id__in=watchlist_ids)
    return render(request, 'pages/watchlist.html', {'assets': assets, 'categories': categories})