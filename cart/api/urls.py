from django.urls import path
from .views import CartItemListCreateAPIView, add_to_cart

urlpatterns = [
    path('cart/items/', CartItemListCreateAPIView.as_view()),
    path('cart/items/add/', add_to_cart)
]