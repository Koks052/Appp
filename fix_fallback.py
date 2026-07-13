with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'r') as f:
    content = f.read()

target = """        val Fallback = SocialStats(
            tiktokFollowers = 428319,
            youtubeSubscribers = 154200,
            discordMembers = 12850
        )"""

replacement = """        val Fallback = SocialStats(
            tiktokFollowers = 3079,
            youtubeSubscribers = 421,
            discordMembers = 128
        )"""

if target in content:
    content = content.replace(target, replacement)

with open('app/src/main/java/com/example/data/network/SocialStatsFetcher.kt', 'w') as f:
    f.write(content)
