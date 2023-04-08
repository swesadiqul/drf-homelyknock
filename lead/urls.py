from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('category', CategoryView),
router.register('question', QuestionsView),
router.register('answer', AnswerView),
router.register('JobPostCreate', JobPostCreate,basename='JobPostCreate'),

urlpatterns = [
    path('', include(router.urls)),
    path('jobpostlistview/', JobPostListView.as_view()),
    path('JobPostListDetail/<int:id>/', JobPostListDetail.as_view()),
    path('JobPostListDelete/<int:id>/', JobPostListDelete.as_view()),
    path('JobPostPerUserView/', JobPostPerUserView.as_view(),name="JobPostPerUserView"),
    path('SendEmailTemplate/', SendEmailTemplate.as_view(),name="SendEmailTemplate"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]



