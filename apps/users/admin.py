from django.contrib import admin
from .models import PasswordReset, UserAccount

admin.site.register(UserAccount)
admin.site.register(PasswordReset)