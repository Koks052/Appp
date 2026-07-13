import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Define the start and end of NotificationsScreen function
start_marker = "fun NotificationsScreen("
end_marker = "fun NotificationItemRow("

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_screen = """fun NotificationsScreen(
    viewModel: KoksixViewModel,
    isAnimationsEnabled: Boolean,
    onAnimationsEnabledChange: (Boolean) -> Unit
) {
    val context = LocalContext.current
    val notifications by viewModel.notifications.collectAsState()
    var isLoggedIn by rememberSaveable { mutableStateOf(true) }

    val lastCheckedTime by viewModel.lastCheckedTime.collectAsState()
    val realLatestVideoTitle by viewModel.realLatestVideoTitle.collectAsState()
    val realLatestTiktokVideoTitle by viewModel.realLatestTiktokVideoTitle.collectAsState()

    val isMusicMuted = BackgroundMusicManager.isMuted
    val selectedSongIndex = BackgroundMusicManager.currentSongIndex
    var isSongDropdownExpanded by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.TopCenter
    ) {
        Column(
            modifier = Modifier
                .widthIn(max = 600.dp)
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp, vertical = 24.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            // Header
            Column(modifier = Modifier.fillMaxWidth()) {
                Text(
                    text = "POWIADOMIENIA",
                    style = MaterialTheme.typography.displayMedium.copy(fontSize = 24.sp, fontWeight = FontWeight.Black),
                    color = Color.White
                )
                Text(
                    text = "Zarządzaj powiadomieniami oraz odtwarzaczem muzyki.",
                    color = TextMuted,
                    fontSize = 13.sp,
                    modifier = Modifier.padding(top = 4.dp)
                )
            }

            // Music Controller
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(
                        BorderStroke(1.dp, if (isMusicMuted) Color.Red.copy(alpha = 0.3f) else NeonPurple.copy(alpha = 0.4f)),
                        RoundedCornerShape(16.dp)
                    ),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = CardBg.copy(alpha = 0.95f))
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(44.dp)
                                .background(if (isMusicMuted) Color.Red.copy(alpha = 0.15f) else NeonPurple.copy(alpha = 0.15f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = if (isMusicMuted) Icons.Default.VolumeOff else Icons.Default.MusicNote,
                                contentDescription = null,
                                tint = if (isMusicMuted) Color.Red else NeonPurpleLight,
                                modifier = Modifier.size(22.dp)
                            )
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "Odtwarzacz Muzyki",
                                color = Color.White,
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = if (isMusicMuted) "Wyciszono" else BackgroundMusicManager.songs.getOrNull(selectedSongIndex)?.name ?: "Wybierz utwór",
                                color = if (isMusicMuted) Color.Red else TextMuted,
                                fontSize = 12.sp
                            )
                        }
                        IconButton(
                            onClick = { BackgroundMusicManager.setMute(context, !isMusicMuted) },
                            modifier = Modifier.size(40.dp)
                        ) {
                            Icon(
                                imageVector = if (isMusicMuted) Icons.Default.VolumeOff else Icons.Default.VolumeUp,
                                contentDescription = null,
                                tint = if (isMusicMuted) Color.Red else NeonGreen
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Song selection dropdown
                    Box(modifier = Modifier.fillMaxWidth()) {
                        Button(
                            onClick = { isSongDropdownExpanded = true },
                            modifier = Modifier.fillMaxWidth().height(44.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color.Black.copy(alpha = 0.3f)),
                            shape = RoundedCornerShape(10.dp),
                            border = BorderStroke(1.dp, NeonPurple.copy(alpha = 0.2f))
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = BackgroundMusicManager.songs.getOrNull(selectedSongIndex)?.name ?: "Wybierz utwór...",
                                    color = Color.White,
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.Medium
                                )
                                Icon(Icons.Default.ArrowDropDown, contentDescription = null, tint = Color.White)
                            }
                        }
                        
                        DropdownMenu(
                            expanded = isSongDropdownExpanded,
                            onDismissRequest = { isSongDropdownExpanded = false },
                            modifier = Modifier.background(CardBg)
                        ) {
                            BackgroundMusicManager.songs.forEachIndexed { index, song ->
                                DropdownMenuItem(
                                    text = {
                                        Column {
                                            Text(
                                                text = song.name,
                                                color = if (index == selectedSongIndex) NeonPurpleLight else Color.White,
                                                fontWeight = if (index == selectedSongIndex) FontWeight.Bold else FontWeight.Normal,
                                                fontSize = 14.sp
                                            )
                                            Text(text = song.description, color = TextMuted, fontSize = 11.sp)
                                        }
                                    },
                                    onClick = {
                                        BackgroundMusicManager.selectSong(context, index)
                                        isSongDropdownExpanded = false
                                        if (isMusicMuted) BackgroundMusicManager.setMute(context, false)
                                    }
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))
                    
                    var musicVolumeMultiplier by remember { mutableStateOf(BackgroundMusicManager.getVolumeMultiplier()) }
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("Głośność (${(musicVolumeMultiplier * 100).toInt()}%)", color = TextMuted, fontSize = 12.sp)
                    }
                    Slider(
                        value = musicVolumeMultiplier,
                        onValueChange = {
                            musicVolumeMultiplier = it
                            BackgroundMusicManager.setVolumeMultiplier(context, it)
                        },
                        valueRange = 0.0f..3.0f,
                        colors = SliderDefaults.colors(
                            thumbColor = NeonPurpleLight,
                            activeTrackColor = NeonPurple,
                            inactiveTrackColor = Color.White.copy(alpha = 0.1f)
                        ),
                        modifier = Modifier.fillMaxWidth().height(24.dp)
                    )
                }
            }

            // Real-Time Social Monitor
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(BorderStroke(1.dp, NeonGreen.copy(alpha = 0.3f)), RoundedCornerShape(16.dp)),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = CardBg.copy(alpha = 0.95f))
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Box(modifier = Modifier.size(10.dp).background(NeonGreen, CircleShape))
                            Text("MONITORING SOCIALI", color = NeonGreen, fontSize = 12.sp, fontWeight = FontWeight.Black, fontFamily = FontFamily.Monospace)
                        }
                        
                        var isRefreshing by remember { mutableStateOf(false) }
                        val scope = rememberCoroutineScope()
                        IconButton(
                            onClick = {
                                if (!isRefreshing) {
                                    isRefreshing = true
                                    scope.launch {
                                        viewModel.performSocialPollAndChecks()
                                        isRefreshing = false
                                        Toast.makeText(context, "Odświeżono!", Toast.LENGTH_SHORT).show()
                                    }
                                }
                            },
                            modifier = Modifier.size(28.dp).background(Color.White.copy(alpha = 0.05f), CircleShape)
                        ) {
                            Icon(Icons.Default.Refresh, contentDescription = null, tint = if (isRefreshing) NeonGreen else Color.White, modifier = Modifier.size(16.dp))
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // YT Row
                    Row(
                        modifier = Modifier.fillMaxWidth().background(Color.Black.copy(alpha = 0.2f), RoundedCornerShape(8.dp)).padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = null, tint = Color(0xFFFF0000), modifier = Modifier.size(24.dp))
                        Spacer(modifier = Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Najnowszy film na YouTube", color = TextMuted, fontSize = 11.sp)
                            Text(realLatestVideoTitle, color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Bold, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // TikTok Row
                    Row(
                        modifier = Modifier.fillMaxWidth().background(Color.Black.copy(alpha = 0.2f), RoundedCornerShape(8.dp)).padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.Movie, contentDescription = null, tint = Color(0xFFFE2C55), modifier = Modifier.size(24.dp))
                        Spacer(modifier = Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Najnowszy TikTok", color = TextMuted, fontSize = 11.sp)
                            Text(realLatestTiktokVideoTitle, color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Bold, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    Text("Ostatnia aktualizacja: $lastCheckedTime", color = TextMuted, fontSize = 10.sp, textAlign = TextAlign.End, modifier = Modifier.fillMaxWidth())
                }
            }

            // Notification History
            Row(
                modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Historia powiadomień (${notifications.size})",
                    color = Color.White,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    if (notifications.any { !it.isRead }) {
                        TextButton(onClick = { viewModel.markAllAsRead() }, contentPadding = PaddingValues(0.dp)) {
                            Text("Przeczytane", color = NeonGreen, fontSize = 13.sp)
                        }
                    }
                    if (notifications.isNotEmpty()) {
                        TextButton(onClick = { viewModel.clearAllNotifications() }, contentPadding = PaddingValues(0.dp)) {
                            Text("Wyczyść", color = Color.Red.copy(alpha = 0.8f), fontSize = 13.sp)
                        }
                    }
                }
            }

            if (notifications.isEmpty()) {
                Card(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.Black.copy(alpha = 0.2f)),
                    shape = RoundedCornerShape(16.dp),
                    border = BorderStroke(1.dp, Color.White.copy(alpha = 0.05f))
                ) {
                    Column(
                        modifier = Modifier.fillMaxWidth().padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Icon(Icons.Outlined.Notifications, contentDescription = null, tint = NeonPurple.copy(alpha = 0.3f), modifier = Modifier.size(48.dp))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Brak powiadomień", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Text("Nowe alerty pojawią się tutaj automatycznie.", color = TextMuted, fontSize = 13.sp, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 6.dp))
                    }
                }
            } else {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    notifications.forEach { item ->
                        NotificationItemRow(
                            item = item,
                            onClick = {
                                viewModel.markAsRead(item)
                                com.example.util.UrlLauncher.launch(context, item.url)
                            },
                            onDelete = {
                                viewModel.deleteNotification(item.firebaseId)
                            },
                            isLoggedIn = isLoggedIn
                        )
                    }
                }
            }
        }
    }
}

@Composable
"""
    
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content[:start_idx] + new_screen + content[end_idx + 26:])
