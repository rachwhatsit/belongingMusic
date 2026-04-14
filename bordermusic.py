import pandas as pd
from midiutil import MIDIFile

# Load your data
df = pd.read_csv("/Users/roycannedy/Desktop/Borders_Data.csv")

# Clean column names
df.columns = [c.strip() for c in df.columns]

# Rename first blank column
df = df.rename(columns={df.columns[0]: "Location"})

# Keep only actual locations, not totals row
df = df[df["Location"] != "TOTALS"].copy()

# Categories to sonify
categories = [
    "Community Only",
    "Friends Only",
    "Family Only",
    "Friends and Family",
    "Family and Community",
    "Friends and Community",
    "All",
    "Other"
]

# Fill missing values with 0
df[categories] = df[categories].fillna(0)


# Helper function
def map_value(value, min_value, max_value, min_result, max_result):
    if max_value == min_value:
        return (min_result + max_result) / 2
    return min_result + (value - min_value) / (max_value - min_value) * (max_result - min_result)


# Flatten all values to get global min/max
all_counts = df[categories].values.flatten()
min_count = all_counts.min()
max_count = all_counts.max()

# Create MIDI
midi = MIDIFile(1)
track = 0
channel = 0
time = 0
tempo = 90
duration = 1

midi.addTempo(track, time, tempo)

# Note set
note_names = [
    60, 62, 64, 67, 69, 72, 74, 76
]  # C major type sound

# Build notes
for _, row in df.iterrows():
    location = row["Location"]

    for i, cat in enumerate(categories):
        count = row[cat]

        # Map counts to pitch index
        pitch_index = round(map_value(count, min_count, max_count, len(note_names) - 1, 0))
        pitch = note_names[pitch_index]

        # Map counts to velocity
        velocity = round(map_value(count, min_count, max_count, 50, 120))

        # Add note
        midi.addNote(track, channel, pitch, time, duration, velocity)

        # Move forward in time
        time += 1

    # Small pause between locations
    time += 2

# Save MIDI file
with open("borders_sonification.mid", "wb") as output_file:
    midi.writeFile(output_file)

print("MIDI file saved as borders_sonification.mid")