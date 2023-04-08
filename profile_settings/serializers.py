from rest_framework import serializers
from profile_settings.models import *
from profile_settings import models
from django.contrib.auth import get_user_model
User = get_user_model()


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id','user','title', 'description','image']


class AboutSerializer(serializers.ModelSerializer):
    company_logo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    profile_image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = About
        fields = [
        'user',
        'company_name',
        'company_logo',
        'profile_image',
        'email',
        'phone',
        'websit_link',
        'location',
        'company_siz',
        'years_of_business',
        'discription',
        'created_at',
        'updated_at',
        ]


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Photo
        fields = [
            'id',
        'user',
        'image',
        'created_at'
        ]

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social_Media_Link
        fields = [
        'user',
        'facebook',
        'twitter',
        'instagram',
        'linkdin',
        'websit_link',
        ]


class Account_DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account_Details
        fields = [
        'user',
        'account_email',
        'usage_contact',
        'sms_notification_number',
        
        ]
        
class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = [
            'id',
            'reviewed_by',
            'reviewed_user',
            'rating',
            'comment',
        ]
        
        # depth=1
class UserSerializer(serializers.ModelSerializer):
    reviews_received = ReviewRatingSerializer(many=True)
    class Meta:
        model = User
        fields =('email','reviews_received',)



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'image', 'credit', 'badges', 'updated_at')


