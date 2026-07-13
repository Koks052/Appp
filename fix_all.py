with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    c = f.read()

c = c.replace("@Composable \nfun NotificationItemRow(", "@Composable")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(c)
