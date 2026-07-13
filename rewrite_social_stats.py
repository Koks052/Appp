import re

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'r') as f:
    content = f.read()

# Fix the broken catch blocks
content = content.replace('${e.message}        // 1.1', '${e.message}")\n        }\n\n        // 1.1')
content = content.replace('${e.message}                // 2.', '${e.message}")\n        }\n\n        // 2.')
content = content.replace('${e.message}        // 3.', '${e.message}")\n        }\n\n        // 3.')
content = content.replace('${e.message}        SocialStats', '${e.message}")\n        }\n\n        SocialStats')

# Fix trailing commas
content = content.replace('latestTiktokVideoId: String? = null,\n    )', 'latestTiktokVideoId: String? = null\n    )')
content = content.replace('latestTiktokVideoId = ttLatestId,\n                    )', 'latestTiktokVideoId = ttLatestId\n        )')
content = content.replace('latestTiktokVideoId = ttLatestId,\n        )', 'latestTiktokVideoId = ttLatestId\n        )')

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'w') as f:
    f.write(content)
