
from typing import Protocol

class FeedParserAbstract(Protocol):
    def get_posts(self, rss_link: str): ...