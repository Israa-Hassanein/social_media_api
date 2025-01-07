from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FollowViewSet, CustomAuthToken, UserViewSet, ProfileViewSet, SomeProtectedView


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'follow', FollowViewSet, basename='follow')  
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('protected/', SomeProtectedView.as_view(), name='protected-endpoint'),
] + router.urls
