from django.contrib import admin

from .models import Account, AccountTier

admin.site.register(Account)
admin.site.register(AccountTier)
