from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.Feed.as_view(), name='feed'),
    path('<int:image_id>/like/', view=views.LikeImage.as_view(), name='like_image'),
    path('<int:image_id>/unlike/', view=views.UnlikeImage.as_view(), name='unlike_image'),
    path('<int:image_id>/comment/', view=views.CommentOnImage.as_view(), name='comment_image'),
    path('comments/<int:comment_id>/', view=views.Comment.as_view(), name='comment'),
    path('search/', view=views.Search.as_view(), name='search'),
]
