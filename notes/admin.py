from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('f_name', 'l_name', 'email')
    list_display_links = ('f_name', 'l_name')


admin.site.register(User, UserAdmin)


