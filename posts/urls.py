from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.PostListAPIView.as_view()),
    path('<str:pk>/detail/', views.PostDetailAPIView.as_view()),
    path('<str:pk>/detail/update/', views.UpdatePostAPIView.as_view()),
    path('<str:pk>/detail/delete/', views.DeletePostAPIView.as_view()),
    path('create/', views.CreatPostAPIView.as_view()),

]