from rest_framework import serializers
from .utils import get_and_authenticate_user
from django.contrib.auth import password_validation, get_user_model
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password')
        if username and password:
            user = get_and_authenticate_user(username, password)
            if not user.is_active:
                error = 'User account is disabled.'
                raise serializers.ValidationError(error)
            data['user'] = user
            return data
        else:
            error = 'Must include username and password'
            raise serializers.ValidationError(error)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=UserModel.objects.all())])

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 'name', 'username')
        extra_kwargs = {
            'password': {'write_only': True},
            'id':  {'required': False, 'read_only': True}
        }

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'username', 'name')
