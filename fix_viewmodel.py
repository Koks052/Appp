import re

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'r') as f:
    content = f.read()

# Remove _realLiveStatus property
content = re.sub(r'private val _realLiveStatus = MutableStateFlow.*?asStateFlow\(\)\n', '', content, flags=re.DOTALL)
content = content.replace("private var lastTiktokLiveStatus: Boolean? = null\n", "")

pattern = re.compile(r'_realLiveStatus\.value = stats\.isTiktokLive\n.*?lastTiktokLiveStatus = stats\.isTiktokLive', re.DOTALL)
content = pattern.sub('', content)

# Remove the word "isTiktokLive" anywhere else just in case
content = content.replace("stats.isTiktokLive", "false")

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'w') as f:
    f.write(content)
