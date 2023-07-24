from rest_framework import viewsets, permissions
from .serializers import FollowSerializer
from posts.models import Follow

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        if self.request.user != serializer.validated_data['following']:
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("You cannot follow yourself.")
