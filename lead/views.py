from django.shortcuts import render
from .models import *
from account.models import *
from .serializers import *
from account.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import FilterSet
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class  = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cat_name__cat']
    
class QuestionsView(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class  = QuestionsSerializer
    filter_backends = [DjangoFilterBackend]
    # global filterset_fields
    # filterset_fields = ['cat']


    
class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class  = AnswerSerializer
    
class JobPostCreate(viewsets.ModelViewSet):
    serializer_class  = PostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        print(self.request.user)
        post_query = Post.objects.all()
        return post_query

    def create(self, request, **kwargs):
        post_data = request.data
        print(post_data)

        post_list = PostList(user = request.user)
        post_list.save()
        
        credit_list = []
        
        for data in post_data:
            print(data['question'])
            post = Post.objects.create(
                post_user = request.user,
                category_id = data['category'],
                question_id = data['question'],
                p_answer_id = data['p_answer'],
            )
            post_list.post_object.add(post)
            
            credit_number = Answer.objects.get(id=data['p_answer'])
            print(credit_number.credit,"credit")
            credit_list.append(credit_number.credit)
        print(sum(credit_list),"credit_list")
        
        post_list.category_id = data['category']
        post_list.location_id = data['location']
        post_list.post_credit = sum(credit_list)
        post_list.save()
       
        serializer = PostSerializer(post)
        return Response(serializer.data)
    

class PostListFilter(FilterSet):
    min_salary = filters.CharFilter(method="filter_by_min_salary")
    max_salary = filters.CharFilter(method="filter_by_max_salary")

    class Meta:
        model = PostList
        fields = ('category','location',)

    def filter_by_min_salary(self, queryset, name, value):
        queryset = queryset.filter(profile__salary__gt=value)
        return queryset

    def filter_by_max_salary(self, queryset, name, value):
        queryset = queryset.filter(profile__salary__lt=value)
        return queryset
    

class JobPostListView(ListAPIView):
    queryset = PostList.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['category','location',]
    # search_fields  = ['location__name']
    # filterset_class = PostListFilter
    
    




class JobPostListDetail(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, id, format=None):
        post_details = PostListSerializer(PostList.objects.get(id=id)).data
        one_click = OneClickResponseSerializer(OneClickResponse.objects.filter(user=request.user),many=True).data
        return Response([post_details, one_click], status=status.HTTP_200_OK)
    
class JobPostListDelete(APIView):
    def get(self, request, id, format=None):
        post_delete = PostList.objects.get(id=id)
        # print(post_delete.post_object.all(),"Delete")
        if post_delete:
            posts = post_delete.post_object.all()
            for post in posts:
                post.delete()
        post_delete.delete()
        return Response({"message":"delete successfull"}, status=status.HTTP_200_OK)
    
        
    

    
    
    
    

        
              
# class JobPostListView(APIView):
    # def get(self, request, format=None):
    #     query = PostList.objects.all()
    #     serializer = PostListSerializer(query,many=True)
    #     filter_class = Django_filter
    #     search_query = self.request.query_params.get('q','')
    #     print(search_query)
    #     result =[]
    #     if search_query:
    #         for i in serializer.data:
    #             for j in i['post_object']:
    #                 print("category name.....",j['category']['name'])
    #                 if j['category']['name'].startswith(search_query):
    #                     result.append(i)
    #                     break              
    #         return Response(result)          
    #     else:      
    #         return Response(serializer.data)  


     
class JobPostPerUserView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, id=None, format=None):
        print(request.user.id)
        queryset = PostList.objects.filter(user = self.request.user)
        print(queryset)
        serializer = PostListSerializer(queryset,many=True)
        return Response(serializer.data)
    

 
class SendEmailTemplate(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        queryset = RecieverEmailTemplate.objects.all()
        serializer = RecieverEmailTemplateSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = RecieverEmailTemplateSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            instance = serializer.save()
            instance.from_user =  request.user
            instance.save()
            
        return Response(serializer.data)






        

    

