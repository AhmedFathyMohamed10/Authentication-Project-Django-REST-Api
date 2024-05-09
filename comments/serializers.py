from rest_framework import serializers
from .models import Comment
from datetime import timedelta


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'post', 'created_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.username
        representation['post'] = instance.post.title
        representation['created_at'] = (instance.created_at + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

        return representation
