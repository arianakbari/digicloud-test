from webapp.ioc import container
from domain.boundaries.input.feed_service_abstract import FeedServiceAbstract

def retry_failed_feeds():
    feed_service = container.resolve(FeedServiceAbstract)
    feed_service.retry_failed_feeds()

def refresh_feeds():
    feed_service = container.resolve(FeedServiceAbstract)
    feed_service.refresh_feeds()

