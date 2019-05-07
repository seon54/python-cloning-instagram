from django.db import models
from nomadgram.users import models as user_models
from nomadgram.images import models as image_models


class Notification(models.Model):
    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )
    
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='noti_creator')
    to = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='noti_to')
    noti_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image, on_delete=models.CASCADE, related_name='noti_image')