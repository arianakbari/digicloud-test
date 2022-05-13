
from domain.boundaries.input.feed_item_service_abstract import FeedItemServiceAbstract
from domain.boundaries.output.feed_item_repository_abstract import FeedItemRepositoryAbstract

class FeedItemService(FeedItemServiceAbstract):
    def __init__(self, feed_item_repository: FeedItemRepositoryAbstract):
        self.feed_item_repository = feed_item_repository

    def get_item(self, **kwargs):
        return self.feed_item_repository.get_item(**kwargs)

    def insert_item(self, feed_id: int, user_id: int, **kwargs):
        item_id = self.feed_item_repository.insert_feed_item(feed_id=feed_id, **kwargs)
        self.feed_item_repository.insert_user_item(feed_item_id=item_id, user_id=user_id)

    def make_as_read_item(self, id: int, user_id: int):
        self.feed_item_repository.make_as_read_item(id, user_id)

    def toggle_favorite(self, id: int, user_id: int):
        self.feed_item_repository.toggle_favorite(id, user_id)

    def toggle_bookmark(self, id: int, user_id: int):
        self.feed_item_repository.toggle_bookmark(id, user_id)

    def get_comments(self, feed_item_id, user_id: int):
        return self.feed_item_repository.get_comments(feed_item_id, user_id)

    def create_comment(self, feed_item_id, **kwargs):
        self.feed_item_repository.create_comment(feed_item_id, **kwargs)
