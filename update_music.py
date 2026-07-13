with open('app/src/main/java/com/example/util/BackgroundMusicManager.kt', 'r') as f:
    content = f.read()

new_songs = """    // Wlazł kotek na płotek
    private val wlazlKotekMelody = listOf(
        Pair(392.00f, 500), // G4
        Pair(329.63f, 500), // E4
        Pair(329.63f, 500), // E4
        Pair(349.23f, 500), // F4
        Pair(293.66f, 500), // D4
        Pair(293.66f, 500), // D4
        Pair(261.63f, 500), // C4
        Pair(329.63f, 500), // E4
        Pair(392.00f, 1000), // G4
        Pair(0.0f, 500)
    )

    // Sto lat
    private val stoLatMelody = listOf(
        Pair(392.00f, 500), // G4
        Pair(329.63f, 500), // E4
        Pair(392.00f, 500), // G4
        Pair(329.63f, 500), // E4
        Pair(392.00f, 500), // G4
        Pair(440.00f, 500), // A4
        Pair(392.00f, 500), // G4
        Pair(349.23f, 500), // F4
        Pair(329.63f, 500), // E4
        Pair(349.23f, 1000), // F4
        Pair(0.0f, 500)
    )

    // Szła dzieweczka do laseczka
    private val szlaDzieweczkaMelody = listOf(
        Pair(261.63f, 500), // C4
        Pair(329.63f, 500), // E4
        Pair(392.00f, 500), // G4
        Pair(392.00f, 500), // G4
        Pair(349.23f, 500), // F4
        Pair(440.00f, 500), // A4
        Pair(392.00f, 1000), // G4
        Pair(0.0f, 500)
    )

    data class Song(val name: String, val author: String, val melody: List<Pair<Float, Int>>)

    val songs = listOf(
        Song("Sweden", "C418", swedenMelody),
        Song("Wet Hands", "C418", wetHandsMelody),
        Song("Subwoofer Lullaby", "C418", subwooferMelody),
        Song("Wlazł kotek", "Polska", wlazlKotekMelody),
        Song("Sto lat", "Tradycyjna", stoLatMelody),
        Song("Szła dzieweczka", "Ludowa", szlaDzieweczkaMelody)
    )"""

import re
pattern = re.compile(r'    data class Song.*?    \)', re.DOTALL)
content = pattern.sub(new_songs, content)

with open('app/src/main/java/com/example/util/BackgroundMusicManager.kt', 'w') as f:
    f.write(content)
