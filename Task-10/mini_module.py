import csv
import math
import random
from pathlib import Path

# --------------------------------------------------
# Task-10: Mini Module Assembly
# --------------------------------------------------

random.seed(42)

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = OUTPUT_DIR / "mini_module_results.csv"

SAMPLE_COUNT = 20
SAMPLE_INTERVAL_MS = 100
SYNC_TOLERANCE_MS = 40

# Configured sensor limits for this demonstration
SENSOR_LIMITS = {
    "temperature": (0.0, 100.0),
    "pressure": (80.0, 120.0),
    "humidity": (0.0, 100.0),
}


def generate_sensor_stream(sensor_name, base_value, offset_ms):
    """Generate synthetic timestamped sensor readings."""

    stream = []

    for i in range(SAMPLE_COUNT):
        timestamp = (
            i * SAMPLE_INTERVAL_MS
            + offset_ms
            + random.randint(-5, 5)
        )

        value = round(base_value + random.uniform(-1.0, 1.0), 2)

        stream.append({
            "timestamp_ms": timestamp,
            "value": value,
        })

    return stream


def inject_test_conditions(streams):
    """Inject known invalid and missing samples."""

    # Invalid temperature reading
    streams["temperature"][5]["value"] = -999.0

    # Missing pressure sample
    streams["pressure"][8]["value"] = None

    # Invalid humidity reading
    streams["humidity"][12]["value"] = 150.0


def find_nearest(stream, reference_timestamp):
    """Find the sample with the nearest timestamp."""

    if not stream:
        return None

    return min(
        stream,
        key=lambda sample: abs(
            sample["timestamp_ms"] - reference_timestamp
        ),
    )


def validate_reading(sensor_name, reading):
    """Check whether a sensor value is present and valid."""

    if reading is None:
        return "DROPOUT"

    if not isinstance(reading, (int, float)):
        return "FAULT"

    if not math.isfinite(reading):
        return "FAULT"

    minimum, maximum = SENSOR_LIMITS[sensor_name]

    if not minimum <= reading <= maximum:
        return "FAULT"

    return "VALID"


def main():
    # 1. Generate the sensor streams
    streams = {
        "temperature": generate_sensor_stream(
            "temperature", 25.0, 0
        ),
        "pressure": generate_sensor_stream(
            "pressure", 101.0, 15
        ),
        "humidity": generate_sensor_stream(
            "humidity", 60.0, -10
        ),
    }

    # 2. Add predefined test cases
    inject_test_conditions(streams)

    # 3. Use temperature timestamps as the reference
    results = []
    last_valid = {
        "temperature": None,
        "pressure": None,
        "humidity": None,
    }

    sync_ok_count = 0
    sync_error_count = 0
    fault_count = 0
    dropout_count = 0

    for index, temperature_sample in enumerate(
        streams["temperature"]
    ):
        reference_timestamp = temperature_sample["timestamp_ms"]

        row = {
            "sample_number": index + 1,
            "reference_timestamp_ms": reference_timestamp,
        }

        matched_samples = {
            "temperature": temperature_sample,
            "pressure": find_nearest(
                streams["pressure"], reference_timestamp
            ),
            "humidity": find_nearest(
                streams["humidity"], reference_timestamp
            ),
        }

        timestamp_differences = []

        for sensor_name, sample in matched_samples.items():
            if sample is None:
                reading = None
                timestamp = None
                difference = None
                status = "DROPOUT"
            else:
                reading = sample["value"]
                timestamp = sample["timestamp_ms"]
                difference = abs(timestamp - reference_timestamp)
                status = validate_reading(sensor_name, reading)

            if difference is not None:
                timestamp_differences.append(difference)

            # Record each sensor's raw data and status.
            row[f"{sensor_name}_timestamp_ms"] = timestamp
            row[f"{sensor_name}_raw"] = reading
            row[f"{sensor_name}_status"] = status

            if status == "VALID":
                last_valid[sensor_name] = reading
                handled_value = reading
            else:
                handled_value = last_valid[sensor_name]

            row[f"{sensor_name}_handled"] = handled_value

            if status == "FAULT":
                fault_count += 1
            elif status == "DROPOUT":
                dropout_count += 1

        # 4. Check synchronization tolerance
        max_difference = max(timestamp_differences, default=0)

        if (
            len(timestamp_differences) == 3
            and max_difference <= SYNC_TOLERANCE_MS
        ):
            sync_status = "SYNCED"
            sync_ok_count += 1
        else:
            sync_status = "OUT_OF_TOLERANCE"
            sync_error_count += 1

        row["max_timestamp_difference_ms"] = max_difference
        row["sync_status"] = sync_status

        results.append(row)

    # 5. Write the integrated results
    fieldnames = list(results[0].keys())

    with OUTPUT_FILE.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # 6. Print the summary
    print("Task-10: Mini Module Assembly")
    print("--------------------------------")
    print(f"Sensor streams: {len(streams)}")
    print(f"Samples per sensor: {SAMPLE_COUNT}")
    print(f"Reference rows: {len(results)}")
    print(f"Synchronization tolerance: {SYNC_TOLERANCE_MS} ms")
    print(f"SYNCED rows: {sync_ok_count}")
    print(f"OUT_OF_TOLERANCE rows: {sync_error_count}")
    print(f"Faulty readings: {fault_count}")
    print(f"Dropout readings: {dropout_count}")
    print(f"CSV output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()