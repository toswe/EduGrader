from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentification.models import User

UserAdmin.fieldsets += (("Custom fields set", {"fields": ("type",)}),)

admin.site.register(User, UserAdmin)
