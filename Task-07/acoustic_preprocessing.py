
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# 1. Configuration
OUTPUT_DIR = Path(__file__).parent
SAMPLE_RATE = 48000
DURATION = 0.05
FREQUENCY = 1000
NOISE_LEVEL = 0.35
WINDOW_SIZE = 5  # Moving-average filter size

# 2. Generate a synthetic acoustic signal
time_axis = np.arange(
    int(SAMPLE_RATE * DURATION)
) / SAMPLE_RATE

clean_signal = np.sin(2 * np.pi * FREQUENCY * time_axis)

# Reproducible noise for testing
rng = np.random.default_rng(42)
noise = rng.normal(0, NOISE_LEVEL, len(time_axis))
noisy_signal = clean_signal + noise

# 3. Apply a moving-average filter
filter_kernel = np.ones(WINDOW_SIZE) / WINDOW_SIZE
filtered_signal = np.convolve(
    noisy_signal, filter_kernel, mode="same"
)

# 4. Windowing: split the signal into fixed-size segments
segment_duration = 0.01  # 10 milliseconds
segment_samples = int(SAMPLE_RATE * segment_duration)

windowed_segments = [
    filtered_signal[i:i + segment_samples]
    for i in range(0, len(filtered_signal), segment_samples)
]

# 5. Save sample-by-sample data to CSV
csv_path = OUTPUT_DIR / "preprocessing_results.csv"

with csv_path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "time_seconds",
        "clean_signal",
        "noisy_signal",
        "filtered_signal"
    ])

    for row in zip(
        time_axis, clean_signal, noisy_signal, filtered_signal
    ):
        writer.writerow(row)

# 6. Plot original, noisy, and filtered signals
plot_path = OUTPUT_DIR / "acoustic_preprocessing.png"

plt.figure(figsize=(12, 7))

plt.subplot(3, 1, 1)
plt.plot(time_axis, clean_signal)
plt.title("Clean Synthetic Acoustic Signal")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(time_axis, noisy_signal)
plt.title("Signal with Added Noise")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(time_axis, filtered_signal)
plt.title("After Moving-Average Filtering")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.savefig(plot_path, dpi=150)
plt.close()

print("=== Acoustic Signal Preprocessing ===")
print(f"Sample rate: {SAMPLE_RATE} Hz")
print(f"Duration: {DURATION} seconds")
print(f"Signal frequency: {FREQUENCY} Hz")
print(f"Filter window size: {WINDOW_SIZE} samples")
print(f"Windowed segments: {len(windowed_segments)}")
print(f"Samples per segment: {segment_samples}")
print(f"CSV saved: {csv_path}")
print(f"Plot saved: {plot_path}")
print("Synthetic signal only; no physical microphone used.")
