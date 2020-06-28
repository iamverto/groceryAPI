from django.urls import path
from .views import CartItemListCreateAPIView

urlpatterns = [
    path('cart/items/', CartItemListCreateAPIView.as_view())
]