from rest_framework import serializers
from .models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    count_comments = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_count_comments(self, obj):
        count = Comment.objects.filter(post=obj).count()
        return f"{count} comments found" if count > 0 else "0 comments found"


    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'count_comments', 'comments')


