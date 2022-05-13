from typing import Protocol


class FeedItemServiceAbstract(Protocol):
    def get_item(self, **kwargs):
        ...

    def insert_item(self, feed_id: int, user_id: int, **kwargs):
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
