import tweepy
import os
import requests
from dotenv import load_dotenv
import praw
import random

load_dotenv()

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
acess_token = os.getenv("acess_token")
acess_secret = os.getenv("acess_secret")
client_id=os.getenv("client_id")
client_secret=os.getenv("client_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acess_token, acess_secret)
api = tweepy.API(auth)

mentions=api.mentions_timeline(count=20)

check=[]

for mention in mentions:
    if mention.id not in check:
        check.append(mention.id)
        screen_name = mention.author.screen_name
        id = mention.id_str
        text=mention.text

        filename = "temp.jpg"
        
        reddit = praw.Reddit(client_id = client_id, 
                     client_secret = client_secret, 
                     user_agent = 'meme-scraper')
        subreddit=reddit.subreddit("dankmemes")
        posts = subreddit.hot(limit=10)
        urls=[post.url for post in posts if "https://v.redd.it" not in post.url and ".gif" not in post.url]
        url=random.sample(urls,k=1)[0]
        print(url)

        request = requests.get(url, stream=True)

        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            image=api.media_upload(filename)
            os.remove(filename)

        media_id=image.media_id_string
        # api.update_status(status='@'+screen_name,in_reply_to_status_id=id,media_ids=[media_id])



