from django.urls import path
from social_app import views


urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetails.as_view()),
    path('users/register', views.UserCreate.as_view()),
    path('user/', views.CurrentUser.as_view()),
]