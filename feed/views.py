from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Feed, FeedItem, FeedItemComment, UserFeedItem
from .serializers import FeedItemCommentSerializer, FeedSerializer
from .tasks import populate_feed
# Create your views here.

class ListCreateFeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all user's feeds with its items
        feeds = Feed.objects.filter(user=request.user).prefetch_related("items").prefetch_related("items__comments")
        data = {
            "success": True,
            "data": FeedSerializer(feeds, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)


    def post(self, request):
        # Create a feed with given link
        link = request.data.get("link", None)
        if link is None:
            return Response(data={ "success": False, "message": "Please provide a link!" }, status=status.HTTP_400_BAD_REQUEST)
        feed_serializer = FeedSerializer(data= {"link": link, "user": request.user.id })
        if feed_serializer.is_valid():
            feed = feed_serializer.save()
            # call the celery task to populate feeds
            populate_feed.delay(feed.id, False)
            return Response(data= {"success": True }, status=status.HTTP_201_CREATED)

        return Response(data={ "success": False, "message": "An error has occurred!" }, status=status.HTTP_400_BAD_REQUEST)

class UpdateDeleteFeedAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        # Force to update the feed with given id
        feed = Feed.objects.filter(id=id, user=request.user).first()
        if not feed:
            return Response(data={"success": False, "message": "Not Found!" }, status=status.HTTP_404_NOT_FOUND)
        # call the celery task to update the feed
        populate_feed.delay(feed.id, True)
        return Response(data={"success": True }, status=status.HTTP_200_OK)


    def delete(self, request, id):
        # Delete a feed with given id
        feed = Feed.objects.filter(id=id, user=request.user).first()
        if not feed:
            return Response(data={"success": False, "message": "Not Found!" }, status=status.HTTP_404_NOT_FOUND)
        feed.delete()
        return Response(data={"success": True }, status=status.HTTP_200_OK)


class ListCreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, feed_item_id):
        comments = FeedItemComment.objects.filter(feed_item_id=feed_item_id, feed_item__feed__user=request.user)
        data = {
            "success": True,
            "data": FeedItemCommentSerializer(comments, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, feed_item_id):
        feed_item = FeedItem.objects.filter(id=feed_item_id, feed__user=request.user).first()
        if not feed_item:
            return Response(data={"success": False, "message": "Not Found!" }, status=status.HTTP_404_NOT_FOUND)
        comment_serializer = FeedItemCommentSerializer(data= { **request.data, "feed_item": feed_item.id })
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(data= {"success": True }, status=status.HTTP_201_CREATED)
        return Response(data={ "success": False, "message": "An error has occurred!" }, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def feed_item_make_as_read(request, feed_item_id):
    user_item = UserFeedItem.objects.filter(user=request.user, feed_item=feed_item_id).first()
    if not user_item:
        return Response(data={"success": False, "message": "Not Found!" }, status=status.HTTP_404_NOT_FOUND)
    user_item.is_read = True
    user_item.save()
    return Response(data={"success": True }, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def feed_item_toggle_favorite(request, feed_item_id):
    user_item = UserFeedItem.objects.filter(user=request.user, feed_item=feed_item_id).first()
    if not user_item:
        return Response(data={"success": False, "message": "Not Found!" }, status=status.HTTP_404_NOT_FOUND)
    user_item.is_favorite = not user_item.is_favorite
    user_item.save()
    return Response(data={"success": True }, status=status.HTTP_200_OK)

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def feed_item_toggle_bookmark(request, feed_item_id):
    user_item = UserFeedItem.objects.filter(user=request.user, feed_item=feed_item_id).first()
    if not user_item:
        return Response(data={"success": False, "message": "Not Found!" }, status=status.HTTP_404_NOT_FOUND)
    user_item.is_bookmarked = not user_item.is_bookmarked
    user_item.save()
    return Response(data={"success": True }, status=status.HTTP_200_OK)