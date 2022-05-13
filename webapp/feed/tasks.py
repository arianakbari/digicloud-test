from celery import shared_task
from webapp.ioc import container
from domain.boundaries.input.feed_service_abstract import FeedServiceAbstract

@shared_task
def populate_feed(id, update_mode):
    feed_service = container.resolve(FeedServiceAbstract)
    feed_service.populate_feed(id, update_mode)
    
