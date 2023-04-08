from django.db import models
from account.models import *
from lead.models import *
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Avg
# Create your models here.

# About
class About(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logo', blank=True, null=True)
    profile_image = models.ImageField(upload_to='company_logo', blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    websit_link = models.URLField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    company_siz = models.CharField(max_length=100, blank=True, null=True)
    years_of_business = models.CharField(max_length=100, blank=True, null=True)
    discription = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.CharField(max_length=100, blank=True, null=True)

    class Meta:

        verbose_name = 'About'
        verbose_name_plural = 'Abouts'

    def __str__(self):
     
        return self.company_name


# Photos
class Photo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to ='uploads/',blank=True, null=True)
    created_at = models.CharField(max_length=100 ,blank=True, null=True)

     

    class Meta:
       
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    # def __str__(self):
        
    #     return self.user.full_name



# bagde
class Badge(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=100 ,blank=True, null=True)
    description = models.CharField(max_length=100 ,blank=True, null=True)
    image = models.ImageField(upload_to ='uploads/',blank=True, null=True)

    class Meta:
        verbose_name = 'Badges'
        verbose_name_plural = 'Badges'


    def __str__(self):
        return self.title
    



# Social_Media_Link
class Social_Media_Link(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    facebook = models.URLField(max_length=100, blank=True, null=True)
    twitter = models.URLField(max_length=100, blank=True, null=True)
    instagram = models.URLField(max_length=100, blank=True, null=True)
    linkdin = models.URLField(max_length=100, blank=True, null=True)
    websit_link = models.URLField(max_length=100, blank=True, null=True)
    created_at = models.URLField(max_length=100, blank=True, null=True)
    updated_at = models.URLField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Social_Media_Link'
        verbose_name_plural = 'Social_Media_Links'

    # def __str__(self):
    #             return self.user.full_name




# Elit_Pro
class Elit_Pro(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    total_views = models.CharField(max_length=100 ,blank=True, null=True)
    total_massege_and_response = models.CharField(max_length=100 ,blank=True, null=True)
    total_search = models.CharField(max_length=100 ,blank=True, null=True)

    class Meta:

        verbose_name = 'Elit_Pro'
        verbose_name_plural = 'Elit_Pro'

    def __str__(self):
        return self.user.full_name


# Account_Details
class Account_Details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    account_email = models.CharField(max_length=100 ,blank=True, null=True)
    usage_contact = models.CharField(max_length=100 ,blank=True, null=True)
    sms_notification_number = models.CharField(max_length=100 ,blank=True, null=True)

    class Meta:

        verbose_name = 'Account_Details'
        verbose_name_plural = 'Account_Details'

    def __str__(self):
        return self.user.full_name


# Review & Ratting

class ReviewRating(models.Model):
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.FloatField()
    comment = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.reviewed_by.full_name} reviewed {self.reviewed_user.full_name}"
    
    class Meta:
        verbose_name_plural = 'ReviewRating'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    image = models.ImageField(upload_to='media/profile', default='images/profile/no_img.png')
    credit = models.IntegerField(default=0, blank=True, null=True)
    badges = models.ManyToManyField(Badge, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Profile"
        db_table = "Profile" 

    def __str__(self):
        return self.user.email

