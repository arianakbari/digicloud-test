from celery import shared_task
from .utils import get_posts_details
from .models import Feed, FeedItem, UserFeedItem

@shared_task
def populate_feed(id, update_mode):
    feed = Feed.objects.filter(id=id).first()
    if not feed:
        return
    data = get_posts_details(feed.link)
    if data is None:
        feed.last_try_success = False
        feed.save()
        return

    if not update_mode:
        feed.title = data['title']
        feed.description = data['description']


    for post in data['posts']:
        try:
            item = FeedItem(**post, feed=feed)
            item.save()
            user_feed_item = UserFeedItem(user=feed.user, feed_item=item)
            user_feed_item.save()
        except:
            feed.last_try_success = False
            feed.save()
            return

    feed.last_try_success = True
    feed.save()
