from django.contrib import admin
from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'pincode', 'street']


admin.site.register(Address, AddressAdmin)
