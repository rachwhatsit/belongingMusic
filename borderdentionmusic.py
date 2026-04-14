import pandas as pd
import numpy as np
from midiutil import MIDIFile
import matplotlib.pyplot as plt

# LOAD DATA
df = pd.read_csv("/Users/roycannedy/Desktop/wacoDetentions.csv")
df.columns = [c.strip() for c in df.columns]

# REMOVE BAD ROWS
df = df[
    df["stay_book_out_date_time"].notna() &
    (df["stay_book_out_date_time"] != 0) &
    (df["stay_book_out_date_time"] != "0") &
    (df["stay_book_out_date_time"] != "")
].copy()

# CONVERT TO DATETIME
df["stay_book_in_date_time"] = pd.to_datetime(df["stay_book_in_date_time"], errors="coerce")
df["stay_book_out_date_time"] = pd.to_datetime(df["stay_book_out_date_time"], errors="coerce")

df = df[
    df["stay_book_in_date_time"].notna() &
    df["stay_book_out_date_time"].notna()
].copy()

# COMPUTE DETENTION DAYS
df["detention_days"] = (
    df["stay_book_out_date_time"] - df["stay_book_in_date_time"]
).dt.total_seconds() / (60 * 60 * 24)

df = df[df["detention_days"] >= 0].copy()
df = df.reset_index(drop=True)
df["person_index"] = range(len(df))

# SCALE TO FIX PITCH CLUMPING
df["detention_days_scaled"] = np.log1p(df["detention_days"])

min_days = df["detention_days_scaled"].min()
max_days = df["detention_days_scaled"].max()

print("Rows after cleaning:", len(df))
print("Raw max detention days:", df["detention_days"].max())
print("Scaled min:", min_days)
print("Scaled max:", max_days)

# HELPER FUNCTION
def map_value(value, min_value, max_value, min_result, max_result):
    if max_value == min_value:
        return (min_result + max_result) / 2
    return min_result + (value - min_value) / (max_value - min_value) * (max_result - min_result)

# VISUAL
plt.scatter(df["person_index"], df["detention_days"])
plt.xlabel("Person Index")
plt.ylabel("Raw Detention Days")
plt.title("People vs Raw Detention Length")
plt.show()

plt.scatter(df["person_index"], df["detention_days_scaled"])
plt.xlabel("Person Index")
plt.ylabel("Scaled Detention Length")
plt.title("People vs Scaled Detention Length")
plt.show()

# CREATE MIDI
midi = MIDIFile(1)
track = 0
channel = 0
tempo = 90
midi.addTempo(track, 0, tempo)

note_names = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]

for _, row in df.iterrows():
    x = row["person_index"]
    y = row["detention_days_scaled"]

    pitch_index = round(map_value(y, min_days, max_days, len(note_names) - 1, 0))
    pitch = note_names[pitch_index]

    velocity = round(map_value(y, min_days, max_days, 50, 120))
    duration = map_value(y, min_days, max_days, 0.25, 2.0)

    time = x * 0.5

    midi.addNote(track, channel, pitch, time, duration, velocity)

with open("waco_detention_sonification_log.mid", "wb") as f:
    midi.writeFile(f)

print("MIDI file saved as waco_detention_sonification_log.mid")

#  OUTPUT
for _, row in df.head(10).iterrows():
    y = row["detention_days_scaled"]

    pitch_index = round(map_value(y, min_days, max_days, len(note_names) - 1, 0))
    pitch = note_names[pitch_index]
    velocity = round(map_value(y, min_days, max_days, 50, 120))
    duration = map_value(y, min_days, max_days, 0.25, 2.0)

    print(
        f"person={row['person_index']}, raw_days={row['detention_days']:.2f}, "
        f"scaled_days={row['detention_days_scaled']:.2f}, "
        f"pitch_index={pitch_index}, pitch={pitch}, "
        f"velocity={velocity}, duration={duration:.2f}"
    )


import os
print("Saved to:", os.path.abspath("waco_detention_sonification_log.mid"))