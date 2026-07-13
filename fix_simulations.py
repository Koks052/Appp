import re

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("        prepopulateSampleNotifications()\n", "")

pattern_prepopulate = re.compile(r'    private fun prepopulateSampleNotifications\(\) \{.*?\n    \}\n', re.DOTALL)
content = pattern_prepopulate.sub('', content)

pattern_trigger = re.compile(r'    fun triggerSimulatedNotification\(.*?\n    \}\n', re.DOTALL)
content = pattern_trigger.sub('', content)

pattern_live_trans = re.compile(r'    fun simulateLiveStatusTransition\(.*?\n    \}\n', re.DOTALL)
content = pattern_live_trans.sub('', content)

pattern_new_yt = re.compile(r'    fun simulateNewYoutubeVideo\(\) \{.*?\n    \}\n', re.DOTALL)
content = pattern_new_yt.sub('', content)

pattern_toggle = re.compile(r'    fun toggleAutoSimulation\(\) \{.*?\n    \}\n', re.DOTALL)
content = pattern_toggle.sub('', content)

pattern_start_auto = re.compile(r'    private fun startAutoSimulationLoop\(\) \{.*?\n    \}\n', re.DOTALL)
content = pattern_start_auto.sub('', content)

with open('app/src/main/java/com/example/viewmodel/KoksixViewModel.kt', 'w') as f:
    f.write(content)
