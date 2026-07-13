with open('app/src/main/java/com/example/data/database/AppDatabase.kt', 'r') as f:
    content = f.read()

content = content.replace('version = 3', 'version = 4')
content = content.replace('.fallbackToDestructiveMigration(true)', '.fallbackToDestructiveMigration()')

with open('app/src/main/java/com/example/data/database/AppDatabase.kt', 'w') as f:
    f.write(content)
