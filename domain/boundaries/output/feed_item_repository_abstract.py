from typing import Protocol


class FeedItemRepositoryAbstract(Protocol):
    def get_item(self, **kwargs):
        ...

    def insert_feed_item(self, **kwargs):
        ...

    def insert_user_item(self, **kwargs):
        ...

    def make_as_read_item(self, id: int, user_id: int):
        ...

    def toggle_favorite(self, id: int, user_id: int):
        ...

    def toggle_bookmark(self, id: int, user_id: int):
        ...

    def get_comments(self, feed_item_id, user_id: int):
        ...

    def create_comment(self, feed_item_id, **kwargs):
        ...
