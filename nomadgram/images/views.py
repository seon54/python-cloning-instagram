from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers


class Feed(APIView):

    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()

        image_list = []

        for follwing_user in following_users:
            user_images = follwing_user.images.all()[:2]

            for image in user_images:
                image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        seralizer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(seralizer.data)
