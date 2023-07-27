from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .serializers import PostSerializer, FollowSerializer, CommentSerializer, GroupSerializer
from posts.models import Post, Follow, Comment, Group


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return user.follower.all()
        return Follow.objects.none()

    def perform_create(self, serializer):
        if self.request.user != serializer.validated_data['following']:
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("You cannot follow yourself.")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def perform_partial_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
