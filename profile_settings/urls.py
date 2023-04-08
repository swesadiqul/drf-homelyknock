from django.urls import path,include
from profile_settings import views

urlpatterns = [
    # begde
    path('begde/', views.begde_list),
    path('begde_detail/<int:pk>/', views.begde_detail),

    # about
    path('about/', views.about_list),
    path('about_detail/<int:pk>/', views.about_detail),

    # photo
    path('photo/', views.photo_list),
    path('photo_detail/<int:pk>/', views.photo_detail),

    # social
    path('social/', views.social_list),
    path('social_detail/<int:pk>/', views.social_detail),

    # User
    
    path('UserFilter/', views.UserFilter.as_view(), name='UserFilter'),
    path('UserFilter/<int:pk>/', views.UserFilter.as_view(), name='UserFilterDetails'),
    # path('<int:pk>/delete/', delete_review, name='delete_review'),
    
    # review_list
    
    path('create_review/', views.CreateReview.as_view(), name='create_review'),
    path('update_review/<pk>/', views.CreateReview.as_view(), name='create_review_details'),

    # Account Details
    path('account_add/', views.Account_Details_list),
    path('account_detail/<int:pk>/', views.account_details_detail),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change_user_type/', views.ChangeUserType.as_view(), name='change_user_type'),
    
]