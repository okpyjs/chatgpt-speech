from acc.models import Account
from django.contrib import admin


# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
