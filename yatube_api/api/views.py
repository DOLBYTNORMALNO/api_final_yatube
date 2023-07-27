from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, viewsets
from rest_framework.exceptions import PermissionDenied

from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Comment, Follow, Group, Post, User


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        search = self.request.query_params.get("search", None)
        if user.is_authenticated:
            queryset = user.follower.all()
            if search is not None:
                queryset = queryset.filter(following__username=search)
            return queryset
        return Follow.objects.none()

    def perform_create(self, serializer):
        following = serializer.validated_data["following"]
        if self.request.user == following:
            raise serializers.ValidationError("You cannot follow yourself.")
        if not User.objects.filter(username=following).exists():
            raise serializers.ValidationError("User does not exist.")
        if Follow.objects.filter(
            user=self.request.user, following=following
        ).exists():
            raise serializers.ValidationError(
                "You are already following this user."
            )
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied(
                "You do not have permission to change this comment."
            )
        serializer.save()

    def perform_partial_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied(
                "You do not have permission to change this comment."
            )
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied(
                "You do not have permission to delete this comment."
            )
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None
