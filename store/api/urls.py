from django.urls import path
from .views import StoreList

urlpatterns = [
    path('stores/', StoreList.as_view()),
]