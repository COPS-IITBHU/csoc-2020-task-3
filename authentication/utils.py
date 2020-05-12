from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token


def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid Credentials")
    return user


def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token.key
