
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def main():
    # Signal configuration
    sample_rate = 48000
    duration = 0.05
    frequency = 1000
    delay_seconds = 0.001  # Simulated 1 ms arrival delay

    # Generate synthetic sound signal
    time_axis = np.arange(
        0, duration, 1 / sample_rate
    )
    signal_1 = np.sin(2 * np.pi * frequency * time_axis)

    # Delay signal for simulated second microphone
    delay_samples = round(delay_seconds * sample_rate)
    signal_2 = np.zeros_like(signal_1)
    signal_2[delay_samples:] = signal_1[:-delay_samples]

    # Estimate TDoA using the known synthetic delay
    estimated_delay = delay_samples / sample_rate
    path_difference = 343 * estimated_delay

    # Save sample-by-sample signal data
    output_csv = Path("Task-06/acoustic_signals.csv")
    with output_csv.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "time_seconds", "mic1_signal", "mic2_signal"
        ])
        writer.writerows(zip(time_axis, signal_1, signal_2))

    # Plot both simulated microphone signals
    plt.figure(figsize=(10, 5))
    plt.plot(time_axis * 1000, signal_1, label="Microphone 1")
    plt.plot(time_axis * 1000, signal_2, label="Microphone 2")
    plt.xlabel("Time (milliseconds)")
    plt.ylabel("Amplitude")
    plt.title("Synthetic Acoustic Signals and Arrival Delay")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Task-06/acoustic_signals.png", dpi=150)
    plt.close()

    print("=== Acoustic Sensing & TDoA Demo ===")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Signal frequency: {frequency} Hz")
    print(f"Simulated delay: {estimated_delay * 1000:.3f} ms")
    print(f"Delay in samples: {delay_samples}")
    print(f"Path-length difference magnitude: {path_difference:.3f} m")
    print(f"CSV saved: {output_csv}")
    print("Plot saved: Task-06/acoustic_signals.png")
    print("Note: This uses synthetic signals and a known delay.")


if __name__ == "__main__":
    main()
