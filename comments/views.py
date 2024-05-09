from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Comment
from .serializers import CommentSerializer

class CommentListAPIView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        count = comments.count()
        if count == 0:
            return Response({'message': 'No comments found.'}, status=status.HTTP_200_OK)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    

class CreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)