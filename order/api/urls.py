from django.urls import path
from .views import OrderList, place_order

urlpatterns = [
    path('orders/', OrderList.as_view()),
    path('orders/place-order/', place_order),
]