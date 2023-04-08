from .models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User,auth
from rest_framework import exceptions
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ValidationError




class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'date_of_birth', 'phone_number', 'corporation_name',  'corporation_number', 'is_professional', 'is_user', 'password']


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordOTPSerializer(serializers.Serializer):
    MEDIA_CHOICES = (
        ('phone', 'Phone'),
        ('email', 'Email'),
    )
    media = serializers.ChoiceField(choices=MEDIA_CHOICES)
    phone_or_email = serializers.CharField(required=True)


class VerifyOTPSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


#service serializers
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id','user', 'service_name', 'service_description']


class ServiceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLocation
        fields = ['id', 'user', 'city', 'distance', 'created', 'updated']


class SMSTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSTemplate
        fields = '__all__'


class EmailTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = EmailTemplate
        fields = ['user','template_name','message']


class OneClickResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneClickResponse
        fields = '__all__'


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'image', 'created_at', 'updated_at']

