from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Feed(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField()
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="feeds", on_delete=models.CASCADE)
    last_try_success = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed, related_name="items", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    guid = models.CharField(max_length=255, null=True, blank=True)
    publish_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} | {self.feed.title}"

class FeedItemComment(models.Model):
    feed_item = models.ForeignKey(FeedItem, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content[:20]} | {self.feed_item.title}"


class UserFeedItem(models.Model):
    user = models.ForeignKey(User, related_name="feed_items", on_delete=models.CASCADE)
    feed_item = models.ForeignKey(FeedItem, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} | {self.feed_item.title}"