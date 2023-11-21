from django.contrib import admin
from .models import Operations, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'username', 'password_row', 'email', )
    list_display = ('id', 'get_full_name', 'username', 'password', 'email', 'calculated_balance')
    list_display_links = ('id', 'username')


    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"



@admin.register(Operations)
class OperationAdmin(admin.ModelAdmin):
    fields = ('user', 'category', 'reason', 'price')
    list_display = ('id', 'user', 'category', 'reason', 'price', 'date_time')
    list_display_links = ('id', 'user', )
    list_filter = ('user', 'category', 'price', 'date_time')
    sortable_by = ('user', 'category', 'price', 'date_time')
