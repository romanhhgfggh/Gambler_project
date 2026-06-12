from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Asset, Category, Broker, SubscriptionPlan, Order
from .forms import ReviewForm, NewsletterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
import yfinance as yf

def home(request, cat_id=None):
    categories = Category.objects.all()
    if cat_id:
        assets = Asset.objects.filter(category_id=cat_id)
        current_category = get_object_or_404(Category, id=cat_id)
        title = f"Категорія: {current_category.title}"
    else:
        assets = Asset.objects.all()
        title = "Всі активи"
        
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
        'title': title,
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

    has_reviewed = False
    if request.user.is_authenticated:
        has_reviewed = asset.reviews.filter(author=request.user.username).exists()
    else:
        has_reviewed = True 

    dynamic_price = asset.price 
    target_ticker = asset.api_ticker if asset.api_ticker else asset.ticker
    try:
        if target_ticker:
            yf_asset = yf.Ticker(target_ticker)
            dynamic_price = round(yf_asset.fast_info['lastPrice'], 4)
    except Exception as e:
        print(f"Помилка API для {target_ticker}: {e}")

    if request.method == 'POST' and 'submit_review' in request.POST:
        if not has_reviewed and request.user.is_authenticated:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.asset = asset
                review.author = request.user.username 
                review.save()
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

def remove_from_watchlist(request, asset_id):
    watchlist = request.session.get('watchlist', [])
    if asset_id in watchlist:
        watchlist.remove(asset_id)
        request.session['watchlist'] = watchlist
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def watchlist_view(request):
    categories = Category.objects.all()
    watchlist_ids = request.session.get('watchlist', [])
    assets = Asset.objects.filter(id__in=watchlist_ids)
    
    # Повертаємо динамічні ціни у Watchlist
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

    return render(request, 'pages/watchlist.html', {'assets': assets, 'categories': categories})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    # Вимога лаби: Адмін бачить ВСІ замовлення ВСІХ людей, звичайний юзер - ТІЛЬКИ СВОЇ
    if request.user.is_superuser:
        orders = Order.objects.all().order_by('-created_at')
        title = "Управління (Всі продажі підписок)"
    else:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        title = "Мої активні підписки"
        
    return render(request, 'pages/profile.html', {'orders': orders, 'title': title})

def pricing_view(request):
    plans = SubscriptionPlan.objects.all()
    user_plans = []
    
    if request.user.is_authenticated:
        user_plans = Order.objects.filter(user=request.user).values_list('plan_id', flat=True)
        
    return render(request, 'pages/pricing.html', {
        'plans': plans, 
        'user_plans': user_plans
    })

@login_required
def checkout_view(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    if Order.objects.filter(user=request.user, plan=plan).exists():
        messages.warning(request, f"У вас вже активовано тариф {plan.title}.")
        return redirect('pricing')

    if request.method == 'POST':
        Order.objects.create(user=request.user, plan=plan)
        return redirect('checkout_success')
        
    return render(request, 'pages/checkout.html', {'plan': plan})

@login_required
def checkout_success_view(request):
    return render(request, 'pages/checkout_success.html')

@login_required
def vip_analytics(request):
    has_subscription = Order.objects.filter(user=request.user).exists()
    
    if request.user.is_superuser or has_subscription:
        return render(request, 'pages/vip_analytics.html')
    else:
        return redirect('pricing')