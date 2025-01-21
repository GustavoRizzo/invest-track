from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('current-datetime/', views.current_datetime, name='current-datetime'),
    path('stock-quote/', views.stock_quote, name='stock-quote'),
    path('companies/', views.companies, name='companies'),
]
