from django.contrib import admin
from .models import UserAccount, Roles, UserSocialAccount
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserSocialAccount)
admin.site.register(Roles)
