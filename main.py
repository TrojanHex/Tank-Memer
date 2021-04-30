import urllib.request, json 
# # with urllib.request.urlopen("https://www.reddit.com/r/dankmemes/hot.json") as url:
# #     data = json.loads(url.read().decode())
# data=[{"Device Name":"abc", "Device Caps":["a1", "b1", "c1"]},
# {"Device Name":"def", "Device Caps":["a2", "b2", "c2"]},
# {"Device Name":"ghi", "Device Caps":["a3", "b3", "c3"]},
# {"Device Name":"jkl", "Device Caps":["a4", "b4", "c4"]}] 

# ndata=json.load(data)
# print(ndata)

# # result=[]
# # for item in data:
# #     my_dict={}
# #     print(item.get('data'))

# # # url="https://www.reddit.com/r/dankmemes/hot.json"


json_url = urllib.request.urlopen("https://www.reddit.com/r/dankmemes/hot.json")

data = json.loads(json_url.read())

data=data['data']['children']
for items in data:
    d={}
    d["images"]=items['data']['url_overridden_by_dest']
    print(d)