from django.contrib import admin
from .models import Operations, User, Category


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'username', 'password', 'email',)
    list_display = ('id', 'get_full_name', 'username', 'password', 'email', 'calculated_balance')
    list_display_links = ('id', 'username')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}   "

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)




@admin.register(Operations)
class OperationAdmin(admin.ModelAdmin):
    fields = ('user', 'typ', 'category', 'amount')
    list_display = ('id', 'user', 'typ', 'category', 'amount', 'date_time')
    list_display_links = ('id', 'user',)
    list_filter = ('user', 'typ', 'amount', 'date_time')
    sortable_by = ('user', 'typ', 'amount', 'date_time')



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('title',)
    list_display = ('id', 'user', 'title',)
    list_display_links = ('user', 'title',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
