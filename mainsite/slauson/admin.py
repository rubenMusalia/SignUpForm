from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = Profile


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)