from django.urls import include, path
from rest_framework import routers

from . import views

# The application name definition
app_name = 'yahoo_finances'

# Module main routes
router = routers.SimpleRouter()
router.register(r'daily-stock-history', views.DailyStockHistoryViewSet)
router.register(r'company', views.CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('company-details/<int:company_id>/', views.company_details, name='company_details'),
    path('multiple-companies/', views.multiple_companies, name='multiple_companies'),
    path('multiple-normalized-companies/', views.multiple_normalized_companies, name='multiple_normalized_companies'),
    path('fixed-data/', views.FixedDataView.as_view(), name='fixed_data'),
]
