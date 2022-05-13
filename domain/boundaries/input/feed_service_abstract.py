from typing import Protocol


class FeedServiceAbstract(Protocol):
    def get_user_feeds(self, user_id: int):
        ...

    def get_feed(self, **kwargs):
        ...

    def create_feed(self, link: str, user_id: int):
        ...

    def update_feed(self, id: int, **kwargs):
        ...

    def get_feed_by_id(self, id: int):
        ...

    def delete_feed(self, id: int):
        ...

    def populate_feed(self, id: int, update_mode: bool):
        ...

    def retry_failed_feeds(self):
        ...

    def refresh_feeds(self):
        ...
