from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.SignUpAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('change-password/', views.ChangePasswordAPIView.as_view()),
    path('users/', views.UserListAPIView.as_view()),
    path('users/my-profile/', views.GetMyProfileAPIView.as_view()),
]
