from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Post

class SocialMediaApiTests(APITestCase):
    def setUp(self):
        # Create a test user and set up test data
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')  # Log in the user

        self.post_data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
        }

    def test_create_post(self):
        """
        Test the creation of a post
        """
        url = reverse('post-list')  # Adjust the URL name to match your post creation endpoint
        response = self.client.post(url, self.post_data, format='json')
        
        # Ensure the post was created successfully and the response status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the post data is in the response
        post = Post.objects.get(id=response.data['id'])
        self.assertEqual(post.title, self.post_data['title'])
        self.assertEqual(post.content, self.post_data['content'])
        self.assertEqual(post.user, self.user)

    def test_get_posts(self):
        """
        Test retrieving all posts
        """
        url = reverse('post-list')  # Adjust the URL name to match your post list endpoint
        self.client.post(url, self.post_data, format='json')  # Create a post
        
        # Fetch all posts
        response = self.client.get(url, format='json')
        
        # Ensure the response is valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one post should exist
        
        # Check that the post's title is returned correctly
        self.assertEqual(response.data[0]['title'], self.post_data['title'])

    def test_follow_user(self):
        """
        Test following a user
        """
        user_to_follow = User.objects.create_user(username='anotheruser', password='testpassword')
        url = reverse('follow', args=[user_to_follow.id])  # Adjust URL name to match your follow endpoint
        
        response = self.client.post(url, format='json')

        # Ensure the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user has successfully followed the other user
        self.user.profile.following.add(user_to_follow)
        self.assertIn(user_to_follow, self.user.profile.following.all())

    def test_feed(self):
        """
        Test fetching a user's feed
        """
        user_to_follow = User.objects.create_user(username='user_to_follow', password='testpassword')
        self.user.profile.following.add(user_to_follow)
        
        # Create a post by the user being followed
        post_data = {
            'title': 'Post by Followed User',
            'content': 'Content of the followed user post.',
            'user': user_to_follow.id,
        }
        url = reverse('post-list')
        self.client.post(url, post_data, format='json')

        # Fetch the feed for the logged-in user
        url = reverse('user-feed')  # Adjust URL name to match your user feed endpoint
        response = self.client.get(url, format='json')

        # Ensure the feed includes posts by followed users
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # The feed should have 1 post
        
        # Verify the post is from the followed user
        self.assertEqual(response.data[0]['user'], user_to_follow.id)
