from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers, models
from nomadgram.notifications import views as notification_views
from nomadgram.users import models as user_models
from nomadgram.users import serializers as user_serializers


class Feed(APIView):

    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()

        image_list = []

        for following_user in following_users:
            user_images = following_user.images.all()[:2]

            for image in user_images:
                image_list.append(image)

        my_images = user.images.all()

        for image in my_images:
            image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        seralizer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(data=seralizer.data)


class LikeImage(APIView):

    def get(self, request, image_id, format=None):
        likes = models.Like.objects.filter(image__id=image_id)
        like_creator_ids = likes.values('creator_id')
        # id__in : array의 user id 검색
        users = user_models.User.objects.filter(id__in=like_creator_ids)
        serailizer = user_serializers.ListUserSerializer(users, many=True)        

        return Response(data=serailizer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisting_like.delete()

            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )      
            notification_views.create_notification(user, found_image.creator, 'like', found_image)
            new_like.save()

            return Response(status=status.HTTP_201_CREATED)


class UnlikeImage(APIView):
    
    def delete(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisting_like.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    '''
    Getting data from front-end to back-end
    '''
    def post(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
 

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=user, image=found_image)
            notification_views.create_notification(user, found_image.creator, 'comment', found_image, serializer.data['message'])

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):

    def delete(self, request, comment_id, format=None):
        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):

    def get(self, request, format=None):

        # type(hashtags) 로 str 타입 확인
        hashtags = request.query_params.get('hashtag', None)
        
        # list로 저장
        if hashtags is not None:
            hashtags = hashtags.split(',')
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()
            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id, format=None):
        user = request.user

        try:
            comment_to_delete = models.Comment.objects.get(
                id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageDetail(APIView):

    # function 인자에 self 잊지 말기
    def find_own_image(self, image_id, user):
        try:
            image = models.Image.objects.get(id=image_id, creator=user)

            return image
        except models.Image.DoesNotExist:

            return None

    def get(self, request, image_id, format=None):
        user = request.user

        try:
            image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ImageSerializer(image)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, image_id, format=None):
        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # partial=True 완료되지 않은 업데이트를 가능하게 함(serializer의 모든 필드 작성하지 않아도 업데이트 가능)
        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id, format=None):
        user = request.user
        image = self.find_own_image(image_id, user)

        if image is None:

            return Response

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)