from django.contrib import admin
from account.models import CustomUser

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cpf', 'telefone']


admin.site.register(CustomUser, UserAdmin)