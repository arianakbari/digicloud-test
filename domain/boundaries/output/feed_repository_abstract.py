from typing import Protocol


class FeedRepositoryAbstract(Protocol):
    def get_feeds_by_user_id(self, user_id: int):
        ...

    def get_feed_by_user_id(self, id: int, user_id: int):
        ...

    def get_feed(self, **kwargs):
        ...

    def get_feeds(self, **kwargs):
        ...

    def insert(self, link: str, user_id: int):
        ...

    def update_feed(self, id: int, **kwargs):
        ...

    def delete_feed(self, id: int):
        ...
