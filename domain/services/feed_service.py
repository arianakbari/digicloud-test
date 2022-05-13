from domain.boundaries.input.feed_item_service_abstract import FeedItemServiceAbstract
from domain.boundaries.input.feed_service_abstract import FeedServiceAbstract
from domain.boundaries.output.feed_parser_abstract import FeedParserAbstract
from domain.boundaries.output.feed_repository_abstract import FeedRepositoryAbstract


class FeedService(FeedServiceAbstract):
    def __init__(
        self,
        feed_repository: FeedRepositoryAbstract,
        feed_item_service: FeedItemServiceAbstract,
        feed_parser: FeedParserAbstract,
    ):
        self.feed_repository = feed_repository
        self.feed_item_service = feed_item_service
        self.feed_parser = feed_parser

    def get_user_feeds(self, user_id: int):
        return self.feed_repository.get_feeds_by_user_id(user_id)

    def get_feed(self, **kwargs):
        return self.feed_repository.get_feed(**kwargs)

    def create_feed(self, link: str, user_id: int) -> id:
        return self.feed_repository.insert(link, user_id)

    def update_feed(self, id: int, **kwargs):
        self.feed_repository.update_feed(id, **kwargs)

    def get_feed_by_id(self, id: int):
        return self.feed_repository.get_feed(id=id)

    def delete_feed(self, id: int):
        self.feed_repository.delete_feed(id)

    def populate_feed(self, id: int, update_mode: bool):
        feed = self.get_feed_by_id(id)
        if not feed:
            return
        data = self.feed_parser.get_posts(feed.link)
        if data is None:
            self.update_feed(feed.id, last_try_success=False)
            return

        if not update_mode:
            self.update_feed(
                feed.id, title=data["title"], description=data["description"]
            )

        for post in data["posts"]:
            try:
                self.feed_item_service.insert_item(feed.id, feed.user_id, **post)
            except:
                self.update_feed(feed.id, last_try_success=False)
                return

        self.update_feed(feed.id, last_try_success=True)

    def retry_failed_feeds(self):
        feeds = self.feed_repository.get_feeds(last_try_success=False)
        for feed in feeds:
            self.populate_feed(feed.id, False)

    def refresh_feeds(self):
        feeds = self.feed_repository.get_feeds()
        for feed in feeds:
            self.populate_feed(feed.id, False)
