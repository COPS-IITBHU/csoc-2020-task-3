from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError



class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # username = serializers.CharField()
    # password = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['username','password',]




    


class RegisterSerializer(serializers.ModelSerializer):
    # TODO: Implement register functionality
    name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ['username','password','email','name']

    def validate(self,data):
        username = data.get('username',None)
        email = data.get('email',None)
        if not email or not username:
            raise ValidationError('Both email and username are required')  
        # users = User.objects.filter(email=email)
        users1 = User.objects.filter(email=email)
        print(users1)
        
        if users1.count() != 0:
            raise ValidationError('A user with same email already exists') 
        return data
    def create(self,data):
        username = data.get('username')
        email = data.get('email')
        name = data.get('first_name')
        password = data.get('password')
        print(username,name,email,password)

        user = User.objects.create_user(username=username,password=password,email=email)  
        user.first_name = name
        user.save()

        return data  

       
    


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ['id','name','username','email',]
    