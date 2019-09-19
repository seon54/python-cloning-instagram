from django.urls import path

from .views import *


urlpatterns = [
    path('', Feed.as_view(), name='feed'),
    path('<int:image_id>/like', LikeImage.as_view(), name='like_image'),
    path('<int:image_id>/unlike', UnlikeImage.as_view(), name='unlike_image'),
    path('<int:image_id>/comment', CommentOnImage.as_view(), name='comment_image'),
    path('comments/<int:comment_id>', Comment.as_view(), name='comment'),

]
