from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, MinLengthValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True, validators=[EmailValidator(message='Enter a valid email address.')]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[MinLengthValidator(8, message='Password must be at least 8 characters long.')]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})

        if attrs.get('email') and User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})

        if attrs.get('username') and User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})

        try:
            validate_password(password)  # Use built-in password validation
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'password': ', '.join(e.messages)})

        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ['username']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user']
        extra_kwargs = {'user': {'read_only': True}}


class ChangePasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')
        extra_kwargs = {'old_password': {'write_only': True}, 'new_password': {'write_only': True}, 'confirm_password': {'write_only': True}}