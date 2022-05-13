from rest_framework import serializers
from .models import Feed, FeedItem, FeedItemComment


class FeedItemCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItemComment
        fields = ["id", "content", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"feed_item": {"write_only": True}}


class FeedItemSerializer(serializers.ModelSerializer):
    comments = FeedItemCommentSerializer(many=True, read_only=True)
    is_read = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = FeedItem
        fields = [
            "link",
            "title",
            "description",
            "created_at",
            "publish_date",
            "id",
            "author",
            "comments",
            "is_read",
            "is_favorite",
            "is_bookmarked",
        ]

    def get_is_read(self, obj):
        return obj.userfeeditem_set.all().first().is_read

    def get_is_favorite(self, obj):
        return obj.userfeeditem_set.all().first().is_favorite

    def get_is_bookmarked(self, obj):
        return obj.userfeeditem_set.all().first().is_bookmarked


class FeedSerializer(serializers.ModelSerializer):
    items = FeedItemSerializer(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ["id", "link", "title", "description", "items", "user"]
        read_only_fields = ["title", "description", "items"]
        extra_kwargs = {"user": {"write_only": True}}
