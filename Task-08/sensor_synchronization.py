
#!/usr/bin/env python3

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Reproducible synthetic sensor data
random.seed(42)

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

START_TIME = datetime(2026, 10, 12, 10, 0, 0)
SAMPLE_COUNT = 20
SAMPLE_INTERVAL_MS = 100
MAX_ALLOWED_DIFFERENCE_MS = 40


def generate_sensor_stream(name, base_value, offset_ms):
    """Generate a sensor stream with timestamp offset and jitter."""
    stream = []

    for i in range(SAMPLE_COUNT):
        jitter_ms = random.randint(-5, 5)
        timestamp = (
            START_TIME
            + timedelta(milliseconds=i * SAMPLE_INTERVAL_MS
                         + offset_ms + jitter_ms)
        )

        stream.append({
            "sensor": name,
            "timestamp": timestamp,
            "value": round(base_value + random.uniform(-2, 2), 2),
        })

    return stream


def find_nearest_reading(stream, target_time):
    """Return the reading closest to a target timestamp."""
    return min(
        stream,
        key=lambda item: abs(
            (item["timestamp"] - target_time).total_seconds()
        ),
    )


def main():
    temperature = generate_sensor_stream(
        "temperature", 28.0, 0
    )
    pressure = generate_sensor_stream(
        "pressure", 101.3, 15
    )
    humidity = generate_sensor_stream(
        "humidity", 60.0, -10
    )

    streams = {
        "temperature": temperature,
        "pressure": pressure,
        "humidity": humidity,
    }

    output_path = OUTPUT_DIR / "synchronized_data.csv"
    tolerance = timedelta(milliseconds=MAX_ALLOWED_DIFFERENCE_MS)

    matched = 0
    unmatched = 0

    with output_path.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "reference_timestamp",
            "temperature",
            "temperature_timestamp",
            "pressure",
            "pressure_timestamp",
            "humidity",
            "humidity_timestamp",
            "status",
        ])

        for temp in temperature:
            target = temp["timestamp"]
            selected = {
                name: find_nearest_reading(stream, target)
                for name, stream in streams.items()
            }

            differences = {
                name: abs(reading["timestamp"] - target)
                for name, reading in selected.items()
            }

            synchronized = all(
                difference <= tolerance
                for difference in differences.values()
            )

            if synchronized:
                matched += 1
            else:
                unmatched += 1

            writer.writerow([
                target.isoformat(timespec="milliseconds"),
                selected["temperature"]["value"],
                selected["temperature"]["timestamp"].isoformat(
                    timespec="milliseconds"
                ),
                selected["pressure"]["value"],
                selected["pressure"]["timestamp"].isoformat(
                    timespec="milliseconds"
                ),
                selected["humidity"]["value"],
                selected["humidity"]["timestamp"].isoformat(
                    timespec="milliseconds"
                ),
                "SYNCED" if synchronized else "OUT_OF_TOLERANCE",
            ])

    print("=== Sensor Synchronization Demo ===")
    print("Sensors:", len(streams))
    print("Samples per sensor:", SAMPLE_COUNT)
    print("Nominal sample interval:", SAMPLE_INTERVAL_MS, "ms")
    print("Maximum allowed difference:", MAX_ALLOWED_DIFFERENCE_MS, "ms")
    print("Reference rows:", SAMPLE_COUNT)
    print("Synchronized rows:", matched)
    print("Out-of-tolerance rows:", unmatched)
    print("CSV saved:", output_path)
    print("Synthetic data only; no physical sensors used.")


if __name__ == "__main__":
    main()
