with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'r') as f:
    content = f.read()

# Remove the clearAllNotifications call
content = content.replace("notificationDao.clearAllNotifications()\n                        notificationDao.insertNotifications(notificationsList)", "notificationDao.insertNotifications(notificationsList)")

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'w') as f:
    f.write(content)
