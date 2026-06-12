from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 100% ГАРАНТІЯ ПЕРЕНАПРАВЛЕННЯ:
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    # --- ВІДНОВЛЕННЯ ПАРОЛЯ ЧЕРЕЗ КАСТОМНІ ШАБЛОНИ В ПАПЦІ registration ---
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
    # ----------------------------------------------------------------------
    
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', include('my_app.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)