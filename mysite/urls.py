"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # Built-in authentication system
from gallery import views  # Assumes your app name is 'gallery'

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),
    
    # Exhibition Core Views
    path('', views.gallery_index, name='gallery_index'),    
    path('upload/', views.upload_image, name='upload_image'),
    path('dashboard/', views.curator_dashboard, name='curator_dashboard'),
    path('edit/<int:pk>/', views.edit_image, name='edit_image'),
    path('delete/<int:pk>/', views.delete_image, name='delete_image'),
    # --- Authentication Dispatch Routes ---
    # Looks for template at templates/registration/login.html by default
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # Logs the user out and redirects them back to the gallery homepage
    path('logout/', auth_views.LogoutView.as_view(next_page='gallery_index'), name='logout'),
]

# CRITICAL: This allows Django to serve media files (uploaded photos) during local testing.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)