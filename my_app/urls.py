from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('category/<int:cat_id>/', views.home, name='category_filter'),
    path('asset/<int:asset_id>/', views.asset_detail, name='assets_detailed'),
]