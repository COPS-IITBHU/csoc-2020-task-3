from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import AddonUser


class AddonUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = AddonUser
    list_display = ['email', 'username', 'name']


admin.site.register(AddonUser, AddonUserAdmin)
