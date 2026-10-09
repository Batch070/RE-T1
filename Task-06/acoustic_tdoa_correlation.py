
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def main():
    sample_rate = 48000
    duration = 0.05
    frequency = 1000
    known_delay_ms = 1.0

    # Generate synthetic microphone signals
    t = np.arange(0, duration, 1 / sample_rate)
    mic1 = np.sin(2 * np.pi * frequency * t)

    delay_samples = round(
        known_delay_ms / 1000 * sample_rate
    )

    mic2 = np.zeros_like(mic1)
    mic2[delay_samples:] = mic1[:-delay_samples]

    # Cross-correlation: estimate relative delay
    correlation = np.correlate(mic2, mic1, mode="full")
    lags = np.arange(-len(mic1) + 1, len(mic2))
    estimated_lag = int(lags[np.argmax(correlation)])

    estimated_delay_s = estimated_lag / sample_rate
    estimated_delay_ms = estimated_delay_s * 1000
    path_difference_m = 343 * abs(estimated_delay_s)

    # Save results
    result_file = Path("Task-06/tdoa_results.csv")
    with result_file.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "known_delay_ms",
            "estimated_delay_ms",
            "estimated_lag_samples",
            "path_difference_m"
        ])
        writer.writerow([
            known_delay_ms,
            estimated_delay_ms,
            estimated_lag,
            path_difference_m
        ])

    # Plot correlation against lag
    plt.figure(figsize=(10, 5))
    plt.plot(lags, correlation)
    plt.axvline(
        estimated_lag,
        linestyle="--",
        label=f"Estimated lag: {estimated_lag} samples"
    )
    plt.xlabel("Lag (samples)")
    plt.ylabel("Cross-correlation")
    plt.title("Cross-Correlation for TDoA Estimation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Task-06/tdoa_correlation.png", dpi=150)
    plt.close()

    print("=== Cross-Correlation TDoA Demo ===")
    print(f"Known delay: {known_delay_ms:.3f} ms")
    print(f"Estimated lag: {estimated_lag} samples")
    print(f"Estimated delay: {estimated_delay_ms:.3f} ms")
    print(f"Estimated path difference magnitude: {path_difference_m:.3f} m")
    print(f"Results saved: {result_file}")
    print("Plot saved: Task-06/tdoa_correlation.png")
    print("Synthetic signals only; no physical microphones used.")


if __name__ == "__main__":
    main()
