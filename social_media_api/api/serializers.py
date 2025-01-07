from rest_framework import serializers
from .models import Post, Follow, Profile, User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'user', 'timestamp', 'media']
        read_only_fields = ['user', 'timestamp']

    def create(self, validated_data):
        # Automatically assign the logged-in user to the post
        user = self.context['request'].user
        print(f"User: {user}") 
        validated_data['user'] = user
        return super().create(validated_data)

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']
        read_only_fields = ['follower']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'profile_picture']

