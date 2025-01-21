from django.urls import path

from .views import LoadDataAPIView

urlpatterns = [
    path('load-data/', LoadDataAPIView.as_view(), name='load_data'),
]
