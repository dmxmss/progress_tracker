#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os

db = "progress.csv"
output_dir = "graphs"

df = pd.read_csv(db)
df["date"] = pd.to_datetime(df["date"])

os.makedirs(output_dir, exist_ok=True)

exercises = df["exercise"].unique()

for exercise in exercises:
    data = df[df["exercise"] == exercise].copy()

    if data["hold_seconds"].notnull().sum() > data["reps"].notnull().sum():
        y_col = "hold_seconds"
        y_label = "Hold seconds"
    else:
        y_col = "reps"
        y_label = "Reps"

    if data[y_col].notnull().sum() < 2:
        print(f"[Missed] not enough data for: {exercise}")
        continue

    data = data.sort_values("date")

    plt.figure(figsize=(10, 6))
    plt.plot(data["date"], data[y_col], marker="o", linestyle="-")
    plt.title(f"Progress: {exercise}")
    plt.xlabel("Date")
    plt.ylabel(y_label)
    plt.grid(True)
    plt.tight_layout()

    filename = exercise.replace(" ", "_").replace("/", "_").lower() + ".png"
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path)
    plt.close()

    print(f"Successfully saved plot for {exercise}")
