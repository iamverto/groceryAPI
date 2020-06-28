from django.urls import path
from .views import user, login, verify_otp, get_address, list_addresses, update_address, add_address, delete_address
urlpatterns = [
    path('auth/user/', user),
    path('auth/login/', login),
    path('auth/verify-otp/', verify_otp),
    path('auth/user/addresses/', list_addresses),
    path('auth/user/addresses/<int:id>/', get_address),
    path('auth/user/addresses/<int:id>/update/', update_address),
    path('auth/user/addresses/<int:id>/delete/', delete_address),
    path('auth/user/addresses/create/', add_address),
]