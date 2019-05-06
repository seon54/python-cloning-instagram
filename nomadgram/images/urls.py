from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.Feed.as_view(), name='feed'),
    path('<image_id>/like/', view=views.LikeImage.as_view(), name='like_image')
]
