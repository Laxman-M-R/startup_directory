from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='companies-home'),
    path('about/', views.about, name = 'companies-about'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]
