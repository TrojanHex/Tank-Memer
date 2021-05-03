import tweepy
import os
import requests
from dotenv import load_dotenv
import praw
import random
import sys
from tweepy.streaming import StreamListener


class Listener(StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(Listener, self).__init__()
        self.output_file = output_file

    def on_status(self, status):
        print("processing image")
        screen_name = status.author.screen_name
        id = status.id_str
        text = status.text.split(" ")

        if len(text) < 2:
            text = "dankmemes"
        else:
            text = text[1]

        filename = "temp.jpg"
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent='meme-scraper')
        try:
            subreddit = reddit.subreddit(text)
            posts = subreddit.hot(limit=10)
            urls = [post.url for post in posts if "https://v.redd.it" not in post.url and ".gif" not in post.url]
            url = random.sample(urls, k=1)[0]

            request = requests.get(url, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
                image = api.media_upload(filename)
                os.remove(filename)
                media_id = image.media_id_string
                api.update_status(status='@'+screen_name,
                                  in_reply_to_status_id=id, media_ids=[media_id])
                print("sent image")
        except Exception as e:
            print(e)

load_dotenv()

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
acess_token = os.getenv("acess_token")
acess_secret = os.getenv("acess_secret")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acess_token, acess_secret)
api = tweepy.API(auth)
mentions = api.mentions_timeline(count=20)
check = []

listener = Listener()

stream = tweepy.Stream(auth=auth, listener=listener)
tweets = stream.filter(track=["@tankmemer"])