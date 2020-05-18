from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='companies-home'),
    path('home/<str:city>', views.home, name='companies-home-city'),
    path('about/', views.about, name = 'companies-about'),
]
