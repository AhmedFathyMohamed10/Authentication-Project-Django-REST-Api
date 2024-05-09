from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CommentListAPIView.as_view()),
    path('add/', views.CreateCommentAPIView.as_view()),

]