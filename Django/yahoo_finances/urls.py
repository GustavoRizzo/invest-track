from django.urls import path

from . import views

# The application name definition
app_name = 'yahoo_finances'

urlpatterns = [
    path('company-details/<int:company_id>/', views.company_details, name='company_details'),
    path('multiple-companies/', views.multiple_companies, name='multiple_companies'),
    path('multiple-normalized-companies/', views.multiple_normalized_companies, name='multiple_normalized_companies'),
]
