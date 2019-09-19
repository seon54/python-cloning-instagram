from rest_framework.serializers import ModelSerializer

from .models import *
from nomadgram.images.serializers import UserProfileImageSerializer


class ExploreUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'profile_image', 'username', 'name',)


class UserProfileSerializer(ModelSerializer):
    images = UserProfileImageSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
            'images',
        )
