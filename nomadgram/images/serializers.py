from rest_framework.serializers import ModelSerializer

from .models import *


class UserProfileImageSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'file', 'comment_count', 'like_count',)


class FeedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'profile_image',)


class CommentSerializer(ModelSerializer):
    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'message', 'creator')


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class ImageSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = Image
        fields = (
            'file',
            'location',
            'caption',
            'creator',
            'created_at',
            'updated_at',
            'comments',
            'like_count',
        )
