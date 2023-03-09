from django.db import models
from django.contrib.auth.models import User


class AccountTier(models.Model):
    name = models.CharField(max_length=50, unique=True)
    thumbnail_sizes = models.CharField(max_length=100)
    original_url = models.BooleanField(default=False)
    expiring_url = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_tier = models.ForeignKey(AccountTier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_tier}"
