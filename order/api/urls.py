from django.urls import path
from .views import OrderList, place_order, OrderDetail, \
    accept_order_by_driver, accept_order_by_store, \
    decline_order_by_driver, decline_order_by_store, deliver_order_by_driver

urlpatterns = [
    path('orders/', OrderList.as_view()),
    path('orders/<int:id>/', OrderDetail.as_view()),
    path('orders/place-order/', place_order),
    path('orders/<int:id>/accept-by-store/', accept_order_by_store),
    path('orders/<int:id>/decline-by-store/', decline_order_by_store),
    path('orders/<int:id>/accept-by-driver/', accept_order_by_driver),
    path('orders/<int:id>/deliver-by-driver/', deliver_order_by_driver),
    path('orders/<int:id>/decline-by-driver/', decline_order_by_driver),
]
