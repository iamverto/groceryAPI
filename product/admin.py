from django.contrib import admin
from .models import Product, ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','description', 'is_active']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)