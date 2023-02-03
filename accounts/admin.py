from django.contrib import admin
from .models import User, FollowRequest

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'is_verified', 'is_private', 'is_superuser', 'is_active']
    search_fields = ['username','email']
    list_filter=['is_active', 'is_verified', 'is_verified']


admin.site.register(User, UserAdmin)
admin.site.register(FollowRequest)

