with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'r') as f:
    content = f.read()

target = """                    _socialStatsState.value = SocialStatsState.Success(stats)
                    _lastCheckedTime.value = java.text.SimpleDateFormat("HH:mm:ss", java.util.Locale.getDefault()).format(java.util.Date())"""

replacement = """                    _socialStatsState.value = SocialStatsState.Success(stats)
                    _lastCheckedTime.value = java.text.SimpleDateFormat("HH:mm:ss", java.util.Locale.getDefault()).format(java.util.Date())
                    _realLatestVideoTitle.value = stats.latestYoutubeVideoTitle ?: "Brak nowych filmów"
"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("Not found target!")

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'w') as f:
    f.write(content)
