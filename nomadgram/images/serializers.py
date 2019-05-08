from rest_framework import serializers
from . import models
from nomadgram.users import models as user_model


class SmallImageSerializer(serializers.ModelSerializer):

    '''Notification에서 사용'''
    class Meta:
        model = models.Image
        fields = (
            'file',
        )        


class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count',
        )


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model.User
        fields = (
            'username',
            'profile_image',
            'name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
            
        )


class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)    # read_only=True 변경불가

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator',
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator',
            'created_at',
        )


class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption',
        )
