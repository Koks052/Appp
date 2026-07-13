import re

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'r') as f:
    content = f.read()

replacement = """FirebaseDatabase.getInstance().getReference("notifications")
            .addChildEventListener(object : com.google.firebase.database.ChildEventListener {
                override fun onChildAdded(snapshot: DataSnapshot, previousChildName: String?) {
                    viewModelScope.launch(Dispatchers.IO) {
                        val notification = NotificationEntity(
                            firebaseId = snapshot.key ?: "",
                            platform = snapshot.child("platform").getValue(String::class.java) ?: "youtube",
                            title = snapshot.child("title").getValue(String::class.java) ?: "",
                            message = snapshot.child("message").getValue(String::class.java) ?: "",
                            url = snapshot.child("url").getValue(String::class.java) ?: "https://www.youtube.com/@koksix_99",
                            timestamp = snapshot.child("timestamp").getValue(Long::class.java) ?: System.currentTimeMillis()
                        )
                        // Tylko dodajemy nowe
                        notificationDao.insertNotification(notification)
                    }
                }
                override fun onChildChanged(snapshot: DataSnapshot, previousChildName: String?) {}
                override fun onChildRemoved(snapshot: DataSnapshot) {
                    viewModelScope.launch(Dispatchers.IO) {
                        snapshot.key?.let { notificationDao.deleteNotificationById(it) }
                    }
                }
                override fun onChildMoved(snapshot: DataSnapshot, previousChildName: String?) {}
                override fun onCancelled(error: DatabaseError) {
                    Log.e("KoksixViewModel", "Firebase notifications listener cancelled", error.toException())
                }
            })"""

# Use regex to replace the old listener
pattern = re.compile(r'FirebaseDatabase\.getInstance\(\)\.getReference\("notifications"\)\n\s*\.addValueEventListener\(object : ValueEventListener \{.*?\n\s*\}\n\s*\}\n\s*override fun onCancelled\(error: DatabaseError\) \{\n\s*Log\.e\("KoksixViewModel", "Firebase notifications listener cancelled", error\.toException\(\)\)\n\s*\}\n\s*\}\)', re.DOTALL)

content = pattern.sub(replacement, content)

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'w') as f:
    f.write(content)
