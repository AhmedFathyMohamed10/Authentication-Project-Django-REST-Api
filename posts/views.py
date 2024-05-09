from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Post
from .serializers import PostSerializer

# Create your views here.
class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        count = posts.count()
        if count == 0:
            return Response({"message": "No posts found"}, status=status.HTTP_200_OK)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    

class PostDetailAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    

class CreatPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdatePostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            return Response({"message": "You are not authorized to update this post"}, status=status.HTTP_403_FORBIDDEN)
        else:
            data = request.data
            serializer = PostSerializer(post, data=data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class DeletePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"message": "You are not authorized to delete this post"}, status=status.HTTP_403_FORBIDDEN)
        else:
            post.delete()
            return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        





