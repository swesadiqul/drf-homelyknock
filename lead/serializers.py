from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question','options','credit']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['question'] = {"qs":instance.question.qs}
        return data
    

class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True,required=False)
    class Meta:
        model = Questions
        fields = ['qs','answers','cat',]
        depth = 1 
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['cat'] = {"name":instance.cat.name,}
    #     return data

class CategorySerializer(serializers.ModelSerializer):
    cat_name = QuestionsSerializer(many=True,required=False)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Category
        fields = ['id','name','image','cat_name','children',]
        # depth = 1
        
    def get_fields(self):
        fields = super().get_fields()
        fields['children'] = CategorySerializer(many=True, read_only=True)
        return fields

             
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['category','question','location','p_answer']
        # depth = 1
    
class PostListSerializer(serializers.ModelSerializer):
    # post_object = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)
    post_object = PostSerializer(many=True)
    class Meta:
        model = PostList
        fields = ('id','user','location','category','post_object','created',)
        
        depth = 1
        
class RecieverEmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecieverEmailTemplate
        fields = '__all__'
        # depth = 1


        

    

    


