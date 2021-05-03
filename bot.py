import tweepy
import os
import requests
from dotenv import load_dotenv
import praw
import random
import pickle
import config
load_dotenv()

# consumer_key = os.getenv("consumer_key")
# consumer_secret = os.getenv("consumer_secret")
# acess_token = os.getenv("acess_token")
# acess_secret = os.getenv("acess_secret")
# client_id=os.getenv("client_id")
# client_secret=os.getenv("client_secret")

consumer_key=config.consumer_key
consumer_secret=config.consumer_secret
acess_secret=config.acess_secret
acess_token=config.acess_token
client_id=config.client_id
client_secret=config.client_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acess_token, acess_secret)
api = tweepy.API(auth)
mentions = api.mentions_timeline(count=20)
check=[]    
# with open('parrot.pkl', 'wb') as f:
#     pickle.dump(mentions.id, f)
if os.path.getsize('all_mentions') > 0:  
    with open('all_mentions', 'rb') as f:
        check = pickle.load(f)
print(check)
for mention in mentions:
    if mention.id not in check:
        print("processing image")
        screen_name = mention.author.screen_name
        id = mention.id_str
        text = mention.text.split(" ") 
        if len(text)<2 :
            text="dankmemes"
        else:
            text=text[1]
        text="dankmemes"
        filename = "temp.jpg"
        reddit = praw.Reddit(client_id = client_id, 
                     client_secret = client_secret, 
                     user_agent = 'meme-scraper')
        subreddit=reddit.subreddit(text)
        posts = subreddit.hot(limit=10)
        urls=[post.url for post in posts if "https://v.redd.it" not in post.url and ".gif" not in post.url]
        url=random.sample(urls,k=1)[0]

        request = requests.get(url, stream=True)
        if request.status_code == 200:
            print("sent image")
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            image = api.media_upload(filename)
            os.remove(filename)
            check.append(mention.id)


        media_id=image.media_id_string
        #api.update_status(status='@'+screen_name,in_reply_to_status_id=id,media_ids=[media_id])
with open('all_mentions', 'wb') as f:
    pickle.dump(check, f)


