from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password





class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=20)