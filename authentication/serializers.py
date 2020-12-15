from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
   class Meta:
       model = UserModel
       fields=('id','username','password',)


class RegisterSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields={"id","name","email","username"}
    