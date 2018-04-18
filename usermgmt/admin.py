# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    can_delete = True
    verbose_name_plural = 'users'
    list_display = ('username', 'password', 'latitude', 'longitude', 'timestamp')

admin.site.register(User, UserAdmin)

