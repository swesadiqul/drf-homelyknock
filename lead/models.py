from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Category(models.Model):
    name= models.CharField(max_length=100)
    parent = models.ForeignKey('self',blank=True, on_delete=models.SET_NULL, null=True ,related_name='children')
    image = models.ImageField(upload_to='category_images/', null=True)
    created=models.DateTimeField(auto_now_add=True,null=True)
    
    def get_categories(self):
        if self.parent is None:
            return self.name
        else:
            return self.parent.get_categories() + ' -> ' + self.name
    
    def __str__(self):
            return self.get_categories()
        
class Location(models.Model):
    name= models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
 
class Questions(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='cat_name')
    qs= models.CharField(max_length=100)
    
    def __str__(self):
        return self.qs


class Answer(models.Model):
    question = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='answers',null=True)
    options= models.CharField(max_length=100)
    credit= models.IntegerField(default=0,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.options}_x_{self.credit}"

    class Meta:
        ordering = ['-id']
              
class Post(models.Model):
    post_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_user',blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='post_category',blank=True,null=True)
    location = models.CharField(max_length=200,blank=True,null=True)
    question = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='post_qs',blank=True,null=True)
    p_answer= models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='post_ans',blank=True,null=True)
    created = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.post_user.email

    class Meta:
        ordering = ['-id']

class PostList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='many_post_user',blank=True,null=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='postlist_location',blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='postlist_category',blank=True,null=True)
    post_object = models.ManyToManyField(Post,related_name='post',blank=True)
    post_credit =  models.IntegerField(null=True)
    created = models.DateTimeField(default=timezone.now())
    
    # def __str__(self):
    #     return self.category.name

    class Meta:
        ordering = ['-id']
    
class RecieverEmailTemplate(models.Model):
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciever_user',blank=True,null=True)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender_user',blank=True,null=True)
    post_list = models.ForeignKey(PostList,on_delete=models.CASCADE,related_name='post_lists',blank=True,null=True)
    template_name = models.CharField(max_length=500)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True,null=True)

    # def __str__(self):
    #     return self.user.to_user +
    


    




