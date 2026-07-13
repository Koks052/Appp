import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace the specific background
content = content.replace("if (realLiveStatus) NeonGreen else Color.Red", "NeonGreen")

tiktok_row_pattern = re.compile(r'\s*// TikTok Status Row.*?Row\([^)]*\)\s*\{\s*Text\(text = "Status Koksix na TikTok:".*?Box\([^)]*\)\s*\{\s*Text\([^)]*\)\s*\}\s*\}', re.DOTALL)

replacement = """
                // YouTube Latest Video Row
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(text = "Najnowszy film na YouTube:", fontSize = 12.sp, color = Color.White)
                    Box(
                        modifier = Modifier
                            .background(
                                NeonPurple.copy(alpha = 0.15f),
                                RoundedCornerShape(4.dp)
                            )
                            .border(
                                BorderStroke(1.dp, NeonPurple.copy(alpha = 0.4f)),
                                RoundedCornerShape(4.dp)
                            )
                            .padding(horizontal = 8.dp, vertical = 2.dp)
                    ) {
                        Text(
                            text = realLatestVideoTitle,
                            color = NeonPurpleLight,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }"""

new_content = tiktok_row_pattern.sub(replacement, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(new_content)

