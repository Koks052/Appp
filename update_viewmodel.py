import re

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'r') as f:
    content = f.read()

replacement = """    private var lastTiktokVideoId: String? = null
    private var lastYoutubeVideoId: String? = null
    private var lastTiktokLiveStatus: Boolean? = null

    private fun startRealTimePolling() {
        viewModelScope.launch(Dispatchers.IO) {
            while (true) {
                try {
                    val stats = statsFetcher.fetchStats()
                    
                    // Update state variables for UI
                    _socialStatsState.value = SocialStatsState.Success(stats)
                    _lastCheckedTime.value = java.text.SimpleDateFormat("HH:mm:ss", java.util.Locale.getDefault()).format(java.util.Date())
                    
                    _realLiveStatus.value = stats.isTiktokLive
                    _realLatestVideoTitle.value = stats.latestYoutubeVideoTitle ?: "Pobieranie..."

                    // 1. Check TikTok Live transition
                    if (lastTiktokLiveStatus != null && lastTiktokLiveStatus != stats.isTiktokLive) {
                        if (stats.isTiktokLive) {
                            triggerRealNotification("tiktok_live", "🔴 Koksix jest na LIVE!", "Odpalaj TikToka! Koksix odpalił live!", "https://www.tiktok.com/@koksixx_")
                        } else {
                            triggerRealNotification("tiktok", "⚫ Koksix zakończył transmisję", "Transmisja dobiegła końca.", "https://www.tiktok.com/@koksixx_")
                        }
                    }
                    lastTiktokLiveStatus = stats.isTiktokLive

                    // 2. Check TikTok Video
                    if (stats.latestTiktokVideoId != null && lastTiktokVideoId != null && stats.latestTiktokVideoId != lastTiktokVideoId) {
                        val title = stats.latestTiktokVideoTitle ?: "Nowy TikTok!"
                        triggerRealNotification("tiktok", "📱 Nowy film na TikToku!", title, "https://www.tiktok.com/@koksixx_")
                    }
                    lastTiktokVideoId = stats.latestTiktokVideoId ?: lastTiktokVideoId

                    // 3. Check Youtube Video
                    if (stats.latestYoutubeVideoId != null && lastYoutubeVideoId != null && stats.latestYoutubeVideoId != lastYoutubeVideoId) {
                        val title = stats.latestYoutubeVideoTitle ?: "Nowy film na YouTube!"
                        triggerRealNotification("youtube", "🎥 Nowy film na YouTube!", title, "https://www.youtube.com/watch?v=${stats.latestYoutubeVideoId}")
                    }
                    lastYoutubeVideoId = stats.latestYoutubeVideoId ?: lastYoutubeVideoId

                } catch (e: Exception) {
                    android.util.Log.e("KoksixViewModel", "Error in polling", e)
                }
                kotlinx.coroutines.delay(20000) // Poll every 20 seconds
            }
        }
    }
    
    private fun triggerRealNotification(platform: String, title: String, message: String, url: String) {
        viewModelScope.launch {
            val notification = NotificationEntity(
                firebaseId = "real_${System.currentTimeMillis()}",
                platform = platform,
                title = title,
                message = message,
                url = url
            )
            notificationDao.insertNotification(notification)
            notificationHelper.showNotification(platform, title, message)
        }
    }"""

pattern = re.compile(r'private fun startRealTimePolling\(\) \{.*?(?=private fun pushSystemNotificationToFirebase)', re.DOTALL)
content = pattern.sub(replacement + "\n\n    ", content)

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'w') as f:
    f.write(content)
