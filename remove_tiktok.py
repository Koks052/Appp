with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "// TikTok Status Row" in line:
        skip = True
    
    if skip and "Spacer(modifier = Modifier.height(6.dp))" in line:
        skip = False
        new_lines.append("""                // YouTube Latest Video Row
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
""")
        continue

    if not skip:
        new_lines.append(line)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.writelines(new_lines)
