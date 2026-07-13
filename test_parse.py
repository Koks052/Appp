import json
bodyString = '{"code":0,"msg":"success","processed_time":0.8046,"data":{"user":{"id":"6795983337849897989"},"stats":{"followingCount":8789,"followerCount":3079,"heartCount":2184,"videoCount":18,"diggCount":0,"heart":2184}}}'
json_obj = json.loads(bodyString)
data = json_obj.get("data")
stats = data.get("stats")
print("Followers:", stats.get("followerCount"))
