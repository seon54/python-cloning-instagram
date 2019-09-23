from django.db import models

from nomadgram.images.models import Image, TimeStampModel
from nomadgram.users.models import User


class Notification(TimeStampModel):
    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.creator} - {self.to}: {self.notification_type}'

