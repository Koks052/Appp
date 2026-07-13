import urllib.request
import urllib.error
req = urllib.request.Request("https://www.tikwm.com/api/user/info/?unique_id=koksixx_", headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(e)
