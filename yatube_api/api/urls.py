from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FollowViewSet, CommentViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'follow', FollowViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='post-comments')
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
