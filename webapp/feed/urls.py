from django.urls import path
from webapp.ioc import get_ioc_view
from . import views



urlpatterns = [
    path("feed-item/<int:feed_item_id>/comment", get_ioc_view(views.ListCreateCommentAPIView)),
    path("feed-item/<int:feed_item_id>/read", get_ioc_view(views.FeedItemMakeAsReadAPIView)),
    path("feed-item/<int:feed_item_id>/favorite", get_ioc_view(views.FeedItemToggleFavoriteAPIView)),
    path("feed-item/<int:feed_item_id>/bookmark", get_ioc_view(views.FeedItemToggleBookmarkAPIView)),
    path("<int:id>", get_ioc_view(views.UpdateDeleteFeedAPIView)),
    path("", get_ioc_view(views.ListCreateFeedAPIView)),
]