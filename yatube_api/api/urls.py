from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet


router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"follow", FollowViewSet, basename="follow")
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    CommentViewSet,
    basename="post-comments",
)
router.register(r"groups", GroupViewSet, basename="groups")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "jwt/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
