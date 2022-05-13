from datetime import datetime
from unittest.mock import patch
from django.test import TestCase
from django.utils.timezone import get_current_timezone
from django.contrib.auth import get_user_model
from domain.services.feed_service import FeedService
from domain.services.feed_item_service import FeedItemService
from .services.feed_repository import FeedRepository
from .services.feed_item_repository import FeedItemRepository
from .models import Feed

User = get_user_model()


class FeedRepositoryTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="Test", password="Test123456")
        self.repository = FeedRepository()

    def test_feed_repository_insert(self):

        link = "http://test.com"

        id = self.repository.insert(link, self.user.id)

        feed = Feed.objects.filter(link=link, user=self.user).first()

        self.assertIsNotNone(feed)
        self.assertEqual(feed.id, id)

    def test_feed_repository_get_feeds(self):
        link1 = "http://test1.com"
        link2 = "http://test2.com"

        feed1 = Feed.objects.create(link=link1, user=self.user)
        feed2 = Feed.objects.create(link=link2, user=self.user)

        feeds = self.repository.get_feeds(user=self.user)

        self.assertNotEqual(len(feeds), 0)
        self.assertEqual(len(feeds), 2)
        self.assertEqual(feeds.first().id, feed1.id)
        self.assertEqual(feeds.last().id, feed2.id)


class FeedServiceTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="Test", password="Test123456")
        self.repository = FeedRepository()

    @patch("webapp.feed.services.feed_repository.FeedRepository")
    def test_feed_service_insert(self, MockFeedRepository):
        link = "http://test.com"
        feed = Feed.objects.create(link=link, user=self.user)

        repository = MockFeedRepository()
        repository.insert.return_value = feed.id

        feed_service = FeedService(repository, None, None)
        result = feed_service.create_feed(link, self.user.id)

        self.assertIsNotNone(result)
        self.assertEqual(result, feed.id)

    @patch("webapp.feed.services.feed_repository.FeedRepository")
    def test_feed_service_get_user_feeds(self, MockFeedRepository):
        link1 = "http://test1.com"
        link2 = "http://test2.com"

        feed1 = Feed.objects.create(link=link1, user=self.user)
        feed2 = Feed.objects.create(link=link2, user=self.user)

        repository = MockFeedRepository()
        repository.get_feeds_by_user_id.return_value = Feed.objects.filter(
            user=self.user
        )

        feed_service = FeedService(repository, None, None)
        result = feed_service.get_user_feeds(self.user.id)

        self.assertNotEqual(len(result), 0)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.first().id, feed1.id)
        self.assertEqual(result.last().id, feed2.id)

    @patch("adapters.feed_parser.FeedParser")
    def test_feed_service_populate_feed(self, MockFeedParser):
        link = "http://test.com"
        feed = Feed.objects.create(link=link, user=self.user)

        feed_parser = MockFeedParser()
        feed_parser.get_posts.return_value = {
            "title": "Title",
            "link": link,
            "description": "Description",
            "posts": [
                {
                    "guid": "Guid 1",
                    "title": "Item Title 1",
                    "description": "Item Desc 1",
                    "author": "Author 1",
                    "link": "http://test-item-1.com",
                    "publish_date": datetime.now(tz=get_current_timezone()),
                },
                {
                    "guid": "Guid 2",
                    "title": "Item Title 2",
                    "description": "Item Desc 2",
                    "author": "Author 2",
                    "link": "http://test-item-2.com",
                    "publish_date": datetime.now(tz=get_current_timezone()),
                },
            ],
        }
        feed_item_service = FeedItemService(FeedItemRepository())
        feed_service = FeedService(FeedRepository(), feed_item_service, feed_parser)

        feed_service.populate_feed(feed.id, False)

        feed = Feed.objects.filter(user=self.user).prefetch_related("items").first()

        self.assertIsNotNone(feed)
        self.assertEqual(feed.title, "Title")
        self.assertEqual(feed.description, "Description")
        self.assertNotEqual(len(feed.items.all()), 0)
        self.assertEqual(len(feed.items.all()), 2)
        self.assertTrue(feed.last_try_success)

    @patch("adapters.feed_parser.FeedParser")
    def test_feed_service_retry_failed_feeds(self, MockFeedParser):
        link = "http://test.com"
        feed = Feed.objects.create(link=link, user=self.user, last_try_success=False)

        feed_parser = MockFeedParser()
        feed_parser.get_posts.return_value = {
            "title": "Title",
            "link": link,
            "description": "Description",
            "posts": [
                {
                    "guid": "Guid 1",
                    "title": "Item Title 1",
                    "description": "Item Desc 1",
                    "author": "Author 1",
                    "link": "http://test-item-1.com",
                    "publish_date": datetime.now(tz=get_current_timezone()),
                },
                {
                    "guid": "Guid 2",
                    "title": "Item Title 2",
                    "description": "Item Desc 2",
                    "author": "Author 2",
                    "link": "http://test-item-2.com",
                    "publish_date": datetime.now(tz=get_current_timezone()),
                },
            ],
        }
        feed_item_service = FeedItemService(FeedItemRepository())
        feed_service = FeedService(FeedRepository(), feed_item_service, feed_parser)

        feed_service.retry_failed_feeds()

        feed = Feed.objects.filter(user=self.user).prefetch_related("items").first()

        self.assertIsNotNone(feed)
        self.assertEqual(feed.title, "Title")
        self.assertEqual(feed.description, "Description")
        self.assertNotEqual(len(feed.items.all()), 0)
        self.assertEqual(len(feed.items.all()), 2)
        self.assertTrue(feed.last_try_success)


class FeedTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="Test", password="Test123456")

    def test_get_feeds_endpoint(self):
        login_response = self.client.post(
            "/api/user/login",
            {"username": "Test", "password": "Test123456"},
            content_type="application/json",
        )
        access_token = login_response.json().get("access", None)

        link = "http://test.com"
        feed = Feed.objects.create(link=link, user=self.user)

        response = self.client.get(
            "/api/feed/", HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        success = response.json().get("success", False)
        data = response.json().get("data", [])

        self.assertEqual(response.status_code, 200)
        self.assertTrue(success)
        self.assertNotEqual(len(data), 0)
        self.assertEqual(len(data), 1)
        self.assertIsNotNone(data[0].get("id"))
