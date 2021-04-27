import tweepy
import os
import requests
from dotenv import load_dotenv


load_dotenv()

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
acess_token = os.getenv("acess_token")
acess_secret = os.getenv("acess_secret")

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
        url = "https://preview.redd.it/d6i4k905snv61.jpg?width=640&height=424&crop=smart&auto=webp&s=bac4a75feb6d00e50139c0b54b1a96aaff877ccf"
        request = requests.get(url, stream=True)

        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            image=api.media_upload(filename)
            os.remove(filename)

        media_id=image.media_id_string
        api.update_status(status='@'+screen_name,in_reply_to_status_id=id,media_ids=[media_id])



