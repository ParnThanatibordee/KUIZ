from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_teacher')
    search_fields = ('email', 'username')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
