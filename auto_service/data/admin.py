from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Car, Customer, Influencer, ServiceMan
from .forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.register(Customer)
admin.site.register(Car)
admin.site.register(Influencer)
admin.site.register(ServiceMan)


class CustomerAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            "username", "email", "first_name", "last_name", "password1", "password2", "skills", "description",
            "start_date"),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'skills', 'description')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions','is_manager','is_teamleader')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')


admin.site.unregister(User)
admin.site.register(User, CustomerAdmin)
