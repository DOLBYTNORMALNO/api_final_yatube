from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Comment, Post, Follow, Group

class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['user', 'following']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'slug', 'description']
        model = Group
