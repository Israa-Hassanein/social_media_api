from .models import Post, Follow, Profile
from .serializers import PostSerializer, FollowSerializer, ProfileSerializer, UserSerializer
from rest_framework import viewsets, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.models import User  # Import User model
from django.utils.dateparse import parse_date
from rest_framework import status



# Home view
def home(request):
    return JsonResponse({"message": "Welcome to the Social Media API!"})


# Custom authentication token class
class CustomAuthToken(ObtainAuthToken):
    """
    Custom Authentication Token view.
    You can extend this if you need to add more data to the response.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # You can add additional data here if needed
        return Response({
            'token': response.data['token'],
            'username': request.user.username,
            'user_id': request.user.id  # Add user ID to the response for clarity
        })


# Login view
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'username': username})
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.filter(follower=user).values_list('following', flat=True)
        queryset = self.queryset.filter(user=user)

        # Filtering by keyword
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(content__icontains=keyword)

        # Filtering by date
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date_parsed = parse_date(start_date)
            end_date_parsed = parse_date(end_date)
            if start_date_parsed and end_date_parsed:
                queryset = queryset.filter(timestamp__range=[start_date_parsed, end_date_parsed])

        # Order by timestamp (reverse chronological order)
        queryset = queryset.order_by('-timestamp')

        return queryset



# Follow view set for managing followers
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.validated_data['following'] == self.request.user:
            raise serializers.ValidationError("You cannot follow yourself.")
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=['post'])
    def unfollow(self, request):
        following_id = request.data.get("following_id")
        try:
            follow_instance = Follow.objects.get(follower=request.user, following_id=following_id)
            follow_instance.delete()
            return JsonResponse({"message": "Successfully unfollowed"})
        except Follow.DoesNotExist:
            return JsonResponse({"error": "You are not following this user"}, status=400)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Check if a profile already exists for the logged-in user
        try:
            profile = Profile.objects.get(user=self.request.user)
            # If profile exists, update it
            serializer = ProfileSerializer(profile, data=serializer.validated_data, partial=True)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            # If no profile exists, create a new one
            serializer.save(user=self.request.user)

# User view set for managing users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # This line should now work since the User model is imported
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class SomeProtectedView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "This is a protected view"})
