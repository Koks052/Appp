with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'r') as f:
    content = f.read()

# Remove TikTok Live from data class
content = content.replace("val isTiktokLive: Boolean = false", "")
content = content.replace("isTiktokLive = ttLive", "")

import re
# Remove the fetching of TikTok live status
tt_live_pattern = re.compile(r'// 1\.2 Fetch TikTok Live Status.*?\} catch \(e: Exception\) \{.*?\}', re.DOTALL)
content = tt_live_pattern.sub('', content)

content = content.replace("var ttLive = false", "")

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'w') as f:
    f.write(content)

