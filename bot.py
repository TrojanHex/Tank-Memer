import tweepy
import os
import requests
from dotenv import load_dotenv
import random

load_dotenv()

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
acess_token = os.getenv("acess_token")
acess_secret = os.getenv("acess_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acess_token, acess_secret)
api = tweepy.API(auth)

mentions = api.mentions_timeline(count=20)
api.mentions_timeline().clear()
# print(dir(mention.user))
check=[]
for mention in mentions:
    print(mention.user.name)
    if mention.id not in check:
        check.append(mention.id)
        screen_name = mention.author.screen_name
        id = mention.id_str
        text = mention.text
        print(mention.id)
        filename = "temp.jpg"
        text="dankmemes"
        data=requests.get("https://www.reddit.com/r/"+text+"/hot.json").json()
        data=data['data']['children']
        d=[]
        for items in data:
            d.append(items['data']['url_overridden_by_dest'])
        url=random.sample(d,k=1)[0]
        print(url)
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            image = api.media_upload(filename)
            os.remove(filename)

        media_id = image.media_id_string
        # api.update_status(status='@'+screen_name,
        #                   in_reply_to_status_id=id, media_ids=[media_id])
