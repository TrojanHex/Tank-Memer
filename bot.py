import tweepy
import os
import requests
# from dotenv import load_dotenv
import praw
import random
import pickle
from sys import argv
# load_dotenv()

consumer_key = argv[1]
consumer_secret = argv[2]
acess_token = argv[3]
acess_secret = argv[4]
client_id=argv[5]
client_secret=argv[6]

print(consumer_key)
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
        
        filename = "temp.jpg"
        reddit = praw.Reddit(client_id = client_id, 
                     client_secret = client_secret, 
                     user_agent = 'meme-scraper')
        try:
            subreddit=reddit.subreddit(text)
            posts = subreddit.hot(limit=10)
            urls=[post.url for post in posts if "https://v.redd.it" not in post.url and ".gif" not in post.url]
            url=random.sample(urls,k=1)[0]

            request = requests.get(url, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
                image = api.media_upload(filename)
                os.remove(filename)
                check.append(mention.id)
                media_id=image.media_id_string
                api.update_status(status='@'+screen_name,in_reply_to_status_id=id,media_ids=[media_id])
                print("sent image")

        except Exception as e:
            print("invalid subreddit name.skipping...")


        
with open('all_mentions', 'wb') as f:
    pickle.dump(check, f)


