with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'r') as f:
    content = f.read()

content = content.replace('")\n        }', '')
content = content.replace('latestTiktokVideoId: String? = null,\n    )', 'latestTiktokVideoId: String? = null\n    )')
content = content.replace('latestTiktokVideoId = ttLatestId,\n        )', 'latestTiktokVideoId = ttLatestId\n        )')

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'w') as f:
    f.write(content)
