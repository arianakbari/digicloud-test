from .models import Feed, FeedItem, UserFeedItem
from .utils import get_posts_details

def retry_failed_feeds():
    failed_feeds = Feed.objects.filter(last_try_success=False)
    for feed in failed_feeds:
        data = get_posts_details(feed.link)
        if data is None:
            feed.last_try_success = False
            feed.save()
            continue

        for post in data['posts']:
            try:
                item = FeedItem(**post, feed=feed)
                item.save()
                user_feed_item = UserFeedItem(user=feed.user, feed_item=item)
                user_feed_item.save()
            except:
                feed.last_try_success = False
                break
        
        if not feed.last_try_success:
            feed.save()
            continue
        
        feed.last_try_success = True
        feed.save()

def refresh_feeds():
    feeds = Feed.objects.filter()
    for feed in feeds:
        data = get_posts_details(feed.link)
        if data is None:
            feed.last_try_success = False
            feed.save()
            continue

        for post in data['posts']:
            try:
                item = FeedItem(**post, feed=feed)
                item.save()
                user_feed_item = UserFeedItem(user=feed.user, feed_item=item)
                user_feed_item.save()
            except:
                feed.last_try_success = False
                break
        
        if not feed.last_try_success:
            feed.save()
            continue
        
        feed.last_try_success = True
        feed.save()

