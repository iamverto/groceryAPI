from django.urls import path
from .views import CartItemListCreateAPIView, add_to_cart, update_cart_item

urlpatterns = [
    path('cart/items/', CartItemListCreateAPIView.as_view()),
    path('cart/items/add/', add_to_cart),
    path('cart/items/update/', update_cart_item),
]