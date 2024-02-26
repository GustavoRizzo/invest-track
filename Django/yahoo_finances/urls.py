from django.urls import path

from . import views

# The application name definition
app_name = 'yahoo_finances'

urlpatterns = [
    path('company-details/<int:company_id>/', views.company_details, name='company_details'),
]
