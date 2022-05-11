from django.urls import path
from . import views



urlpatterns = [
    path("feed-item/<int:feed_item_id>/comment", views.ListCreateCommentAPIView.as_view()),
    path("feed-item/<int:feed_item_id>/read", views.feed_item_make_as_read),
    path("feed-item/<int:feed_item_id>/favorite", views.feed_item_toggle_favorite),
    path("feed-item/<int:feed_item_id>/bookmark", views.feed_item_toggle_bookmark),
    path("<int:id>", views.UpdateDeleteFeedAPIView.as_view()),
    path("", views.ListCreateFeedAPIView.as_view()),
]