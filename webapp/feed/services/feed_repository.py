from domain.boundaries.output.feed_repository_abstract import FeedRepositoryAbstract
from webapp.feed.models import Feed

class FeedRepository(FeedRepositoryAbstract):
    def get_feeds_by_user_id(self, user_id: int):
        return Feed.objects.filter(user=user_id).prefetch_related("items").prefetch_related("items__comments")

    def get_feed_by_user_id(self, id: int, user_id: int):
        return Feed.objects.filter(id=id, user=user_id).first()

    def get_feed(self, **kwargs):
        return Feed.objects.filter(**kwargs).first()

    def get_feeds(self, **kwargs):
        return Feed.objects.filter(**kwargs)

    def insert(self, link: str, user_id: int):
        return Feed.objects.create(link=link, user_id=user_id).id

    def update_feed(self, id: int, **kwargs):
        Feed.objects.filter(id=id).update(**kwargs)

    def delete_feed(self, id: int):
        Feed.objects.filter(id=id).delete()
