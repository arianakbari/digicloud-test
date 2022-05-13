from django.db.models import Q
from domain.boundaries.output.feed_item_repository_abstract import FeedItemRepositoryAbstract
from webapp.feed.models import FeedItem, FeedItemComment, UserFeedItem


class FeedItemRepository(FeedItemRepositoryAbstract):

    def get_item(self, **kwargs):
        return FeedItem.objects.filter(**kwargs).first()

    def insert_feed_item(self, **kwargs):
        return FeedItem.objects.create(**kwargs).id

    def insert_user_item(self, **kwargs):
        return UserFeedItem.objects.create(**kwargs).id

    def make_as_read_item(self, id: int, user_id: int):
        UserFeedItem.objects.filter(user=user_id, feed_item=id).update(is_read=True)

    def toggle_favorite(self, id: int, user_id: int):
        UserFeedItem.objects.filter(user=user_id, feed_item=id).update(is_favorite=Q(is_favorite=False))

    def toggle_bookmark(self, id: int, user_id: int):
        UserFeedItem.objects.filter(user=user_id, feed_item=id).update(is_bookmarked=Q(is_bookmarked=False))

    def get_comments(self, feed_item_id, user_id: int):
        return FeedItemComment.objects.filter(feed_item_id=feed_item_id, feed_item__feed__user=user_id)

    def create_comment(self, feed_item_id, **kwargs):
        FeedItemComment.objects.create(feed_item_id=feed_item_id, **kwargs)