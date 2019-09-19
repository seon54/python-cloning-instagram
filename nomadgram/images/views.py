from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


class Feed(APIView):

    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()

        image_list = []

        for following_user in following_users:
            user_image = following_user.images.all()[:2]

            for image in user_image:
                image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        serializer = ImageSerializer(sorted_list, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LikeImage(APIView):

    def post(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            preexisting_like = Like.objects.get(creator=user, image=found_image)
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except Like.DoesNotExist:
            new_like = Like.objects.create(creator=user, image=found_image)
            new_like.save()

        return Response(status=status.HTTP_201_CREATED)


class UnlikeImage(APIView):

    def delete(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            preexisting_like = Like.objects.get(creator=user, image=found_image)
            preexisting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user, image=found_image)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):

    def delete(self, request, comment_id, format=None):
        user = request.user
        try:
            comment = Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
