from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['mobile']


admin.site.register(User, UserAdmin)