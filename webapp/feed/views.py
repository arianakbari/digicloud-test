from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from domain.boundaries.input.feed_item_service_abstract import FeedItemServiceAbstract
from domain.boundaries.input.feed_service_abstract import FeedServiceAbstract
from .serializers import FeedItemCommentSerializer, FeedSerializer
from .tasks import populate_feed

# Create your views here.


@method_decorator(csrf_exempt, name="dispatch")
class ListCreateFeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, feed_service: FeedServiceAbstract):
        self.feed_service = feed_service

    def get(self, request):
        # Get all user's feeds with its items
        feeds = self.feed_service.get_user_feeds(request.user.id)
        data = {"success": True, "data": FeedSerializer(feeds, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a feed with given link
        link = request.data.get("link", None)
        if link is None:
            return Response(
                data={"success": False, "message": "Please provide a link!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        feed_id = self.feed_service.create_feed(link, request.user.id)
        populate_feed.delay(feed_id, False)

        return Response(data={"success": True}, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateDeleteFeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, feed_service: FeedServiceAbstract):
        self.feed_service = feed_service

    def post(self, request, id):
        # Force to update the feed with given id
        feed = self.feed_service.get_feed(id=id, user=request.user.id)
        if not feed:
            return Response(
                data={"success": False, "message": "Not Found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # call the celery task to update the feed
        populate_feed.delay(feed.id, True)
        return Response(data={"success": True}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        # Delete a feed with given id
        feed = self.feed_service.get_feed(id=id, user=request.user.id)
        if not feed:
            return Response(
                data={"success": False, "message": "Not Found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        self.feed_service.delete_feed(feed.id)
        return Response(data={"success": True}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class ListCreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, feed_item_service: FeedItemServiceAbstract):
        self.feed_item_service = feed_item_service

    def get(self, request, feed_item_id):
        comments = self.feed_item_service.get_comments(feed_item_id, request.user.id)
        data = {
            "success": True,
            "data": FeedItemCommentSerializer(comments, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, feed_item_id):
        feed_item = self.feed_item_service.get_item(
            id=feed_item_id, feed__user=request.user
        )
        if not feed_item:
            return Response(
                data={"success": False, "message": "Not Found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        self.feed_item_service.create_comment(feed_item_id, **request.data)
        return Response(data={"success": True}, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name="dispatch")
class FeedItemMakeAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, feed_item_service: FeedItemServiceAbstract):
        self.feed_item_service = feed_item_service

    def post(self, request, feed_item_id):
        self.feed_item_service.make_as_read_item(feed_item_id, request.user.id)
        return Response(data={"success": True}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class FeedItemToggleFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, feed_item_service: FeedItemServiceAbstract):
        self.feed_item_service = feed_item_service

    def post(self, request, feed_item_id):
        self.feed_item_service.toggle_favorite(feed_item_id, request.user.id)
        return Response(data={"success": True}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class FeedItemToggleBookmarkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, feed_item_service: FeedItemServiceAbstract):
        self.feed_item_service = feed_item_service

    def post(self, request, feed_item_id):
        self.feed_item_service.toggle_bookmark(feed_item_id, request.user.id)
        return Response(data={"success": True}, status=status.HTTP_200_OK)
