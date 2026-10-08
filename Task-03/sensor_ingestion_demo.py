#!/usr/bin/env python3

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

RAW_FILE = BASE_DIR / "raw_sensor_data.csv"
VALID_FILE = BASE_DIR / "valid_sensor_data.csv"
REJECTED_FILE = BASE_DIR / "rejected_sensor_data.csv"


VALID_SENSORS = {
    "TEMP_01": ("TEMPERATURE", "C"),
    "PRESS_01": ("PRESSURE", "kPa"),
    "HUM_01": ("HUMIDITY", "%"),
    "ACCEL_01": ("ACCELERATION", "m/s2"),
}

VALID_STATUS = {"OK", "WARN", "ERROR"}


def generate_sensor_packets(count=20):
    """Generate reproducible synthetic sensor packets."""

    random.seed(42)

    packets = []
    start_time = datetime(2026, 10, 7, 10, 0, 0)

    for i in range(count):
        sensor_id = random.choice(list(VALID_SENSORS.keys()))
        sensor_type, unit = VALID_SENSORS[sensor_id]

        if sensor_type == "TEMPERATURE":
            value = round(random.uniform(20, 35), 2)
        elif sensor_type == "PRESSURE":
            value = round(random.uniform(98, 103), 2)
        elif sensor_type == "HUMIDITY":
            value = round(random.uniform(40, 80), 2)
        else:
            value = round(random.uniform(8, 12), 2)

        timestamp = start_time + timedelta(seconds=i)
        status = random.choice(["OK", "OK", "OK", "WARN"])

        packet = (
            f"{sensor_id}|"
            f"{timestamp.isoformat()}|"
            f"{sensor_type}|"
            f"{value}|"
            f"{unit}|"
            f"{status}"
        )

        packets.append(packet)

    # Intentionally invalid packets for validation testing
    packets.append(
        "TEMP_01|2026-10-07T10:00:21|TEMPERATURE|ABC|C|OK"
    )

    packets.append(
        "TEMP_01|2026-10-07T10:00:22|TEMPERATURE|29.5|C"
    )

    packets.append(
        "UNKNOWN_01|2026-10-07T10:00:23|TEMPERATURE|25.0|C|OK"
    )

    return packets


def parse_and_validate(packet):
    """Parse and validate a raw sensor packet."""

    fields = packet.split("|")

    if len(fields) != 6:
        return None, "Invalid number of fields"

    sensor_id, timestamp, sensor_type, value, unit, status = fields

    if sensor_id not in VALID_SENSORS:
        return None, "Unknown sensor ID"

    expected_type, expected_unit = VALID_SENSORS[sensor_id]

    if sensor_type != expected_type:
        return None, "Sensor type mismatch"

    if unit != expected_unit:
        return None, "Unit mismatch"

    if status not in VALID_STATUS:
        return None, "Invalid status"

    try:
        numeric_value = float(value)
    except ValueError:
        return None, "Sensor value is not numeric"

    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        return None, "Invalid timestamp"

    data = {
        "timestamp": timestamp,
        "sensor_id": sensor_id,
        "sensor_type": sensor_type,
        "value": numeric_value,
        "unit": unit,
        "status": status,
    }

    return data, "Valid"


def save_raw_data(packets):
    """Save raw sensor packets."""

    with open(RAW_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["raw_packet"])

        for packet in packets:
            writer.writerow([packet])


def save_processed_data(valid_data, rejected_data):
    """Save validated and rejected sensor data."""

    fields = [
        "timestamp",
        "sensor_id",
        "sensor_type",
        "value",
        "unit",
        "status",
    ]

    with open(VALID_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(valid_data)

    with open(REJECTED_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["raw_packet", "reason"])

        for packet, reason in rejected_data:
            writer.writerow([packet, reason])


def main():
    print("=== RE-T1 Sensor Data Ingestion Demo ===")

    packets = generate_sensor_packets()

    save_raw_data(packets)

    valid_data = []
    rejected_data = []

    for packet in packets:
        data, result = parse_and_validate(packet)

        if data is not None:
            valid_data.append(data)
        else:
            rejected_data.append((packet, result))

    save_processed_data(valid_data, rejected_data)

    print(f"\nTotal packets      : {len(packets)}")
    print(f"Valid packets      : {len(valid_data)}")
    print(f"Rejected packets   : {len(rejected_data)}")

    print("\nOutput files:")
    print(f"Raw data           : {RAW_FILE}")
    print(f"Valid data         : {VALID_FILE}")
    print(f"Rejected data      : {REJECTED_FILE}")

    print("\nRejected packet details:")

    for packet, reason in rejected_data:
        print(f"- {reason}: {packet}")

    print("\nSensor ingestion pipeline completed successfully.")


if __name__ == "__main__":
    main()
