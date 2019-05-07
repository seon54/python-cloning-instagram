from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


class Notifications(APIView):
    
    def get(self, request, foramt=None):
        user = request.user
        notification = models.Notification.objects.filter(to=user)
        serializer = serializers.NotificationSerializer(notification, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


def create_notification(creator ,to, type, image=None, comment=None):
    notification = models.Notification.objects.create(
        creator=creator,
        to=to,
        noti_type=type,
        image=image,
        comment=comment,
    )
    notification.save()