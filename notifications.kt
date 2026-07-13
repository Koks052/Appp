// 2. NOTIFICATIONS SCREEN (The Requested Feature)
// ==========================================
@Composable
fun NotificationsScreen(
    viewModel: KoksixViewModel,
    isAnimationsEnabled: Boolean,
    onAnimationsEnabledChange: (Boolean) -> Unit
) {
    val context = LocalContext.current
    val notifications by viewModel.notifications.collectAsState()
    
    // Auth state (to allow admin actions - temporarily enabled for all users)
    var isLoggedIn by rememberSaveable { mutableStateOf(true) }

    // Real-time states
    val lastCheckedTime by viewModel.lastCheckedTime.collectAsState()
    val realLatestVideoTitle by viewModel.realLatestVideoTitle.collectAsState()
    val realLatestTiktokVideoTitle by viewModel.realLatestTiktokVideoTitle.collectAsState()

    // Music states
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
                .padding(16.dp)
        ) {
        // Tab header
        Column(modifier = Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = "📬 POWIADOMIENIA",
                style = MaterialTheme.typography.displayMedium.copy(fontSize = 20.sp, textAlign = TextAlign.Center),
                color = Color.White
            )
            Text(
                text = "Sprawdzaj najnowsze nagrania na YT/TikTok oraz status transmisji LIVE!",
                color = TextMuted,
                fontSize = 12.sp,
                modifier = Modifier.padding(top = 4.dp, bottom = 12.dp),
                textAlign = TextAlign.Center
            )
        }


        // --- ANIMATIONS CONTROLLER CARD (LOCKED ALWAYS-ON) ---
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 12.dp)
                .border(BorderStroke(1.dp, NeonPurple.copy(alpha = 0.4f)), RoundedCornerShape(12.dp)),
            shape = RoundedCornerShape(12.dp),
            colors = CardDefaults.cardColors(containerColor = CardBg.copy(alpha = 0.9f))
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    Box(
                        modifier = Modifier
                            .size(38.dp)
                            .background(NeonPurple.copy(alpha = 0.2f), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Star,
                            contentDescription = "Animations state",
                            tint = NeonPurpleLight,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                    Column {
                        Text(
                            text = "Efekty wizualne w tle",
                            fontSize = 13.sp,
                            color = Color.White,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Zabezpieczone: ZAWSZE WŁĄCZONE ✨",
                            fontSize = 11.sp,
                            color = NeonGreen,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }

                Button(
                    onClick = {
                        Toast.makeText(
                            context,
                            "Zabezpieczenie: Animacje w tle muszą pozostać aktywne dla klimatu aplikacji!",
                            Toast.LENGTH_SHORT
                        ).show()
                    },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = NeonPurple.copy(alpha = 0.6f)
                    ),
                    shape = RoundedCornerShape(8.dp),
                    contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Text(
                        text = "AKTYWNE 🔒",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        fontFamily = FontFamily.Monospace,
                        color = Color.White
                    )
                }
            }
        }

        // --- BACKGROUND MUSIC CONTROLLER CARD ---
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 12.dp)
                .border(
                    BorderStroke(
                        1.dp, 
                        if (isMusicMuted) Color.Red.copy(alpha = 0.25f) else NeonPurple.copy(alpha = 0.4f)
                    ), 
                    RoundedCornerShape(12.dp)
                ),
            shape = RoundedCornerShape(12.dp),
            colors = CardDefaults.cardColors(containerColor = CardBg.copy(alpha = 0.9f))
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                        modifier = Modifier.weight(1f)
                    ) {
                        Box(
                            modifier = Modifier
                                .size(38.dp)
                                .background(
                                    if (isMusicMuted) Color.Red.copy(alpha = 0.12f) else NeonPurple.copy(alpha = 0.2f), 
                                    CircleShape
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = if (isMusicMuted) Icons.Default.VolumeOff else Icons.Default.MusicNote,
                                contentDescription = "Music icon",
                                tint = if (isMusicMuted) Color.Red else NeonPurpleLight,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                        Column {
                            Text(
                                text = "Muzyka klimatyczna w tle",
                                fontSize = 13.sp,
                                color = Color.White,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = if (isMusicMuted) "Wyciszona (Kliknij odcisz)" else "Utwór: ${BackgroundMusicManager.songs.getOrNull(selectedSongIndex)?.name ?: "Brak"}",
                                fontSize = 11.sp,
                                color = if (isMusicMuted) Color.Red.copy(alpha = 0.8f) else NeonPurpleLight,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }

                    // Mute/Unmute Switch Button
                    IconButton(
                        onClick = {
                            val newMute = !isMusicMuted
                            BackgroundMusicManager.setMute(context, newMute)
                        },
                        modifier = Modifier
                            .background(
                                if (isMusicMuted) Color.Red.copy(alpha = 0.15f) else NeonGreen.copy(alpha = 0.15f),
                                RoundedCornerShape(8.dp)
                            )
                            .border(
                                BorderStroke(
                                    1.dp,
                                    if (isMusicMuted) Color.Red.copy(alpha = 0.4f) else NeonGreen.copy(alpha = 0.4f)
                                ),
                                RoundedCornerShape(8.dp)
                            )
                            .size(36.dp)
                    ) {
                        Icon(
                            imageVector = if (isMusicMuted) Icons.Default.VolumeOff else Icons.Default.VolumeUp,
                            contentDescription = "Toggle Mute",
                            tint = if (isMusicMuted) Color.Red else NeonGreen,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))

                // Song selection row / dropdown
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = "Wybierz utwór:",
                        fontSize = 11.sp,
                        color = TextMuted,
                        fontFamily = FontFamily.Monospace
                    )

                    Box {
                        Button(
                            onClick = { isSongDropdownExpanded = true },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color.Black.copy(alpha = 0.4f)
                            ),
                            border = BorderStroke(1.dp, NeonPurple.copy(alpha = 0.3f)),
                            shape = RoundedCornerShape(8.dp),
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                            modifier = Modifier.height(32.dp)
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(4.dp)
                            ) {
                                Text(
                                    text = BackgroundMusicManager.songs.getOrNull(selectedSongIndex)?.name ?: "Wybierz...",
                                    fontSize = 11.sp,
                                    color = Color.White,
                                    fontWeight = FontWeight.Bold,
                                    fontFamily = FontFamily.Monospace
                                )
                                Icon(
                                    imageVector = Icons.Default.ArrowDropDown,
                                    contentDescription = "Expand songs list",
                                    tint = Color.White,
                                    modifier = Modifier.size(16.dp)
                                )
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
                                                fontSize = 13.sp
                                            )
                                            Text(
                                                text = song.description,
                                                color = TextMuted,
                                                fontSize = 10.sp
                                            )
                                        }
                                    },
                                    onClick = {
                                        BackgroundMusicManager.selectSong(context, index)
                                        isSongDropdownExpanded = false
                                        // Auto-unmute when selecting a song so user hears it
                                        if (isMusicMuted) {
                                            BackgroundMusicManager.setMute(context, false)
                                        }
                                    }
                                )
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))
                HorizontalDivider(color = Color.White.copy(alpha = 0.1f), thickness = 0.5.dp)
                Spacer(modifier = Modifier.height(10.dp))

                var musicVolumeMultiplier by remember { mutableStateOf(BackgroundMusicManager.getVolumeMultiplier()) }

                Column(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Głośność tła (Wzmocnienie o dodatkowe 100%):",
                            fontSize = 11.sp,
                            color = TextMuted,
                            fontFamily = FontFamily.Monospace
                        )
                        Text(
                            text = "${(musicVolumeMultiplier * 100).toInt()}%",
                            fontSize = 11.sp,
                            color = if (musicVolumeMultiplier > 1.0f) NeonPurpleLight else Color.White,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace
                        )
                    }

                    Spacer(modifier = Modifier.height(4.dp))

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
                            inactiveTrackColor = Color.White.copy(alpha = 0.15f)
                        ),
                        modifier = Modifier.fillMaxWidth().height(24.dp)
                    )
                }
            }
        }

        // --- REAL-TIME LIVE & YT/TIKTOK CHECKER STATUS PANEL ---
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 12.dp)
                .border(BorderStroke(1.dp, NeonGreen.copy(alpha = 0.25f)), RoundedCornerShape(12.dp)),
            shape = RoundedCornerShape(12.dp),
            colors = CardDefaults.cardColors(containerColor = CardBg.copy(alpha = 0.9f))
        ) {
            Column(
                modifier = Modifier.padding(12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Box(
                            modifier = Modifier
                                .size(8.dp)
                                .background(NeonGreen, CircleShape)
                        )
                        Text(
                            text = "MONITORING SOCIALI",
                            fontSize = 11.sp,
                            color = NeonGreen,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace
                        )
                    }
 
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Text(
                            text = "Auto-sprawdzanie: co 20s",
                            fontSize = 9.sp,
                            color = TextMuted,
                            fontFamily = FontFamily.Monospace
                        )
                        
                        var isRefreshing by remember { mutableStateOf(false) }
                        val scope = rememberCoroutineScope()
                        
                        IconButton(
                            onClick = {
                                if (!isRefreshing) {
                                    isRefreshing = true
                                    scope.launch {
                                        viewModel.performSocialPollAndChecks()
                                        isRefreshing = false
                                        Toast.makeText(context, "Zaktualizowano dane monitoringowe!", Toast.LENGTH_SHORT).show()
                                    }
                                }
                            },
                            modifier = Modifier.size(24.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Refresh,
                                contentDescription = "Refresh",
                                tint = if (isRefreshing) NeonGreen else Color.White,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                    }
                }
 
                Spacer(modifier = Modifier.height(10.dp))
 
                // YouTube Latest Video Row
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Najnowszy film na YouTube:", 
                        fontSize = 12.sp, 
                        color = Color.White,
                        modifier = Modifier.weight(1.2f)
                    )
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .background(
                                NeonPurple.copy(alpha = 0.15f),
                                androidx.compose.foundation.shape.RoundedCornerShape(4.dp)
                            )
                            .border(
                                androidx.compose.foundation.BorderStroke(1.dp, NeonPurple.copy(alpha = 0.4f)),
                                androidx.compose.foundation.shape.RoundedCornerShape(4.dp)
                            )
                            .padding(horizontal = 8.dp, vertical = 2.dp)
                    ) {
                        Text(
                            text = realLatestVideoTitle,
                            color = NeonPurpleLight,
                            fontSize = 11.sp,
                            fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                            fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                        )
                    }
                }
                Spacer(modifier = Modifier.height(6.dp))
 
                // YouTube Latest Video Row Detailed
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(6.dp))
                        .background(Color.Black.copy(alpha = 0.2f))
                        .padding(8.dp)
                ) {
                    Text(
                        text = "OSTATNI FILM NA YT:",
                        fontSize = 9.sp,
                        color = TextMuted,
                        fontFamily = FontFamily.Monospace
                    )
                    Text(
                        text = realLatestVideoTitle,
                        fontSize = 12.sp,
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1
                    )
                }
 
                Spacer(modifier = Modifier.height(12.dp))

                // TikTok Latest Video Row
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Najnowszy film na TikToku:", 
                        fontSize = 12.sp, 
                        color = Color.White,
                        modifier = Modifier.weight(1.2f)
                    )
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .background(
                                Color(0xFFFE2C55).copy(alpha = 0.15f),
                                androidx.compose.foundation.shape.RoundedCornerShape(4.dp)
                            )
                            .border(
                                androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFFE2C55).copy(alpha = 0.4f)),
                                androidx.compose.foundation.shape.RoundedCornerShape(4.dp)
                            )
                            .padding(horizontal = 8.dp, vertical = 2.dp)
                    ) {
                        Text(
                            text = realLatestTiktokVideoTitle,
                            color = Color(0xFFFE2C55),
                            fontSize = 11.sp,
                            fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                            fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                        )
                    }
                }
                Spacer(modifier = Modifier.height(6.dp))
 
                // TikTok Latest Video Row Detailed
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(6.dp))
                        .background(Color.Black.copy(alpha = 0.2f))
                        .padding(8.dp)
                ) {
                    Text(
                        text = "OSTATNI FILM NA TIKTOKU:",
                        fontSize = 9.sp,
                        color = TextMuted,
                        fontFamily = FontFamily.Monospace
                    )
                    Text(
                        text = realLatestTiktokVideoTitle,
                        fontSize = 12.sp,
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1
                    )
                }

                Spacer(modifier = Modifier.height(10.dp))
 
                // Last updated timestamp
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Ostatnia aktualizacja:",
                        fontSize = 11.sp,
                        color = TextMuted
                    )
                    Text(
                        text = lastCheckedTime,
                        color = Color.White,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        fontFamily = FontFamily.Monospace
                    )
                }
            }
        }

        // Actions Header Row
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Historia powiadomień (${notifications.size})",
                color = Color.White,
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold
            )

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                if (notifications.any { !it.isRead }) {
                    TextButton(onClick = { viewModel.markAllAsRead() }) {
                        Text("Przeczytane", color = NeonGreen, fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                    }
                }
                if (notifications.isNotEmpty()) {
                    TextButton(onClick = { viewModel.clearAllNotifications() }) {
                        Text("Wyczyść", color = Color.Red.copy(alpha = 0.8f), fontSize = 12.sp, fontFamily = FontFamily.Monospace)
                    }
                }
            }
        }

        // Notification List or Empty State
        Box(
            modifier = Modifier
                .fillMaxWidth()
        ) {
            if (notifications.isEmpty()) {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 16.dp),
                    colors = CardDefaults.cardColors(containerColor = CardBg.copy(alpha = 0.5f)),
                    border = BorderStroke(1.dp, NeonPurple.copy(alpha = 0.1f)),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Notifications,
                            contentDescription = null,
                            tint = NeonPurple.copy(alpha = 0.35f),
                            modifier = Modifier.size(56.dp)
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = "Brak powiadomień",
                            color = Color.White,
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Nowe powiadomienia pojawią się automatycznie, gdy tylko zostaną opublikowane na kanale lub TikToku.",
                            color = TextMuted,
                            fontSize = 12.sp,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.padding(top = 4.dp)
                        )
                    }
                }
            } else {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(10.dp)
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
}

@Composable
fun NotificationItemRow(
    item: NotificationEntity,
    onClick: () -> Unit,
    onDelete: () -> Unit,
    isLoggedIn: Boolean
) {
    val platformColor = when (item.platform) {
        "youtube" -> Color(0xFFFF0000)
        "tiktok" -> Color(0xFF000000)
        else -> NeonPurpleLight // "tiktok_live"
    }

    val platformIcon = when (item.platform) {
        "youtube" -> Icons.Default.PlayArrow
        "tiktok" -> Icons.Default.Movie
        else -> Icons.Default.Sensors
    }

    val formatter = remember { SimpleDateFormat("HH:mm · dd.MM.yyyy", Locale.getDefault()) }
    val formattedDate = remember(item.timestamp) { formatter.format(Date(item.timestamp)) }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .border(
                BorderStroke(1.dp, if (!item.isRead) platformColor.copy(alpha = 0.4f) else Color.White.copy(alpha = 0.05f)),
                RoundedCornerShape(12.dp)
            ),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = CardBg.copy(alpha = 0.85f))
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(14.dp)
