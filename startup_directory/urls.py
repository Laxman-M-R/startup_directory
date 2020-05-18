"""startup_directory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from companies import views as company_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('companies.urls')),
    path('register/', company_views.register, name='register'),
    path('profile/', company_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='companies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='companies/logout.html'), name='logout'),
    path('password-reset/',
          auth_views.PasswordResetView.as_view(
            template_name='companies/password_reset.html'
          ),
          name='password_reset'),
    path('password-reset/done/',
          auth_views.PasswordResetDoneView.as_view(
            template_name='companies/password_reset_done.html'
          ),
          name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(
            template_name='companies/password_reset_confirm.html'
          ),
          name='password_reset_confirm'),
    path('password-reset-complete',
          auth_views.PasswordResetCompleteView.as_view(
            template_name='companies/password_reset_complete.html'
          ),
          name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
