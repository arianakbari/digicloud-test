import feedparser
import requests
from io import BytesIO
from dateutil import parser

def get_posts_details(rss=None):
    
    """
    Take link of rss feed as argument
    """
    if rss is not None:
        # Do request using requests library and timeout
        try:
            resp = requests.get(rss, timeout=20.0)
        except:
            return

        # Put it to memory stream object universal feedparser
        content = BytesIO(resp.content)
        # parsing blog feed
        feed = feedparser.parse(content)
          
        # getting lists of blog entries via .entries
        posts = feed.entries
          
        # dictionary for holding posts details
        posts_details = {
            "title": feed.feed.get("title"), 
            "link": feed.feed.get("link"), 
            "description": feed.feed.get("description")
        }
          
        post_list = []
          
        # iterating over individual posts
        for post in posts:
            temp = dict()
              
            # if any post doesn't have information then throw error.
            temp["guid"] = post.get("id", None)
            temp["title"] = post.get("title", None)
            temp["description"] = post.get("description", None)
            temp["link"] = post.get("link", None)
            temp["author"] = post.get("author", None)
            temp["publish_date"] = parser.parse(post.get("published", None))
            
              
            post_list.append(temp)
          
        # storing lists of posts in the dictionary
        posts_details["posts"] = post_list
          
        return posts_details # returning the details which is dictionary
    else:
        return None
  
# if __name__ == "__main__":
#   import json
  
#   feed_url = "https://www.khabaronline.ir/rss"
  
#   data = get_posts_details(rss = feed_url) # return blogs data as a dictionary
    
#   if data:
#     # printing as a json string with indentation level = 2
#     print(json.dumps(data, indent=2))
#   else:
#     print("None")