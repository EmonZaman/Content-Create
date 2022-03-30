from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name',  'is_active', 'is_staff']
    fieldsets = [
        [None, {'fields': ['username', 'password']}],
        [_('Personal info'), {'fields': ['first_name', 'last_name', 'email','country','profile_pic','secondary_email','phone','content_choice','gender','is_pro','pro_expiry_date','facebook','linked_in',
                                         'full_name',
                                         'age',
                                         'language',

                                         ]}],
        [_('Permissions'), {
            'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'],
        }],
        [_('Important dates'), {'fields': ['last_login', 'date_joined']}],
    ]
    date_hierarchy = 'date_joined'


admin.site.register(Permission)