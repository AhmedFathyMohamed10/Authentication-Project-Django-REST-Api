from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post
from comments.models import Comment

class PostListAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post1 = Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        self.post2 = Post.objects.create(title='Post 2', content='Content 2', author=self.user)
        Comment.objects.create(post=self.post1, author=self.user, content='Comment 1')
        Comment.objects.create(post=self.post1, author=self.user, content='Comment 2')

    def test_get_posts_list(self):
        """
        Test retrieving a list of posts.
        """
        response = self.client.get('/api/posts/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 

        # Check the content of the first post
        self.assertEqual(response.data[0]['title'], 'Post 1')
        self.assertEqual(response.data[0]['content'], 'Content 1')
        self.assertEqual(response.data[0]['author'], 'testuser')
        self.assertEqual(response.data[0]['count_comments'], '2 comments found')
        self.assertEqual(len(response.data[0]['comments']), 2)

        # Check the content of the second post (no comments)
        self.assertEqual(response.data[1]['title'], 'Post 2')
        self.assertEqual(response.data[1]['count_comments'], '0 comments found')
        self.assertEqual(len(response.data[1]['comments']), 0) 

    def test_get_empty_posts_list(self):
        """
        Test when there are no posts in the database.
        """
        Post.objects.all().delete()
        response = self.client.get('/api/posts/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "No posts found"})