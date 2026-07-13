import re

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'val requestVid = Request.Builder\(\).*?\.build\(\)', re.DOTALL)

replacement = """val playlistId = channelId.replaceFirst("UC", "UU")
            val requestVid = Request.Builder()
                .url("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=$playlistId&maxResults=1&key=$apiKey")
                .header("User-Agent", "Mozilla/5.0")
                .build()"""

content = pattern.sub(replacement, content)

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'w') as f:
    f.write(content)

