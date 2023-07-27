from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post, Follow, Group, User
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False
    )

    class Meta:
        fields = "__all__"
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("post",)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ["user", "following"]
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["user", "following"],
                message="You are already following this user.",
            )
        ]

    def validate_following(self, value):
        if self.context["request"].user == value:
            raise serializers.ValidationError("You cannot follow yourself.")
        return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "title", "slug", "description"]
        model = Group
