import re

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'val idObj = firstItem.optJSONObject\("id"\).*?val snippet = firstItem.optJSONObject\("snippet"\).*?ytLatestTitle = snippet\?\.optString\("title"\)', re.DOTALL)

replacement = """val snippet = firstItem.optJSONObject("snippet")
                            val resourceId = snippet?.optJSONObject("resourceId")
                            ytLatestId = resourceId?.optString("videoId")
                            ytLatestTitle = snippet?.optString("title")"""

content = pattern.sub(replacement, content)

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'w') as f:
    f.write(content)

