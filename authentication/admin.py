from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_admin', 'date_joined')
    list_filter = ('is_admin',)

    BASE_FIELDS = (None, {'fields': ('email', 'password',)})
    INFORMATION_FIELDS = ('User information', {'fields': ('username',)})
    PERMISSION_FIELDS = ('Permissions and accessibility settings ',
                         {'fields': ('groups', 'user_permissions', 'is_admin', 'is_superuser', 'is_active',)})
    fieldsets = (BASE_FIELDS, INFORMATION_FIELDS, PERMISSION_FIELDS,)

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
