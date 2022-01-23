from django.contrib import admin
from .models import  User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# Register your models here.

class UserAdmin(DjangoUserAdmin):
    readonly_fields = ('created_at','updated_at')
    list_display = ('id','username','is_superuser', 'is_owner', 'is_staff','archive',)


admin.site.register(User,UserAdmin)