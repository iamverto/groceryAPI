from django.urls import path
from .views import DriverList, DriverDetail

urlpatterns = [
    path('drivers/', DriverList.as_view()),
    path('drivers/<int:id>/', DriverDetail.as_view()),
]