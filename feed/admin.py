from django.contrib import admin
from .models import Feed, FeedItem, FeedItemComment, UserFeedItem

# Register your models here.

admin.site.register(Feed)
admin.site.register(FeedItem)
admin.site.register(FeedItemComment)
admin.site.register(UserFeedItem)
