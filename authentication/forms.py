from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AddonUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = AddonUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = AddonUser
        fields = UserChangeForm.Meta.fields
