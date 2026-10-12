
import csv
import math
from pathlib import Path

# Configuration
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 100.0

# None represents a missing sensor reading.
# -999 and 150 are deliberately invalid test values.
sensor_readings = [
    25.2,
    25.4,
    25.7,
    None,
    26.0,
    -999.0,
    26.3,
    150.0,
    26.5,
    None,
    26.8,
    27.0,
]

output_file = Path(__file__).with_name("fault_dropout_results.csv")

last_valid_reading = None
valid_count = 0
fault_count = 0
dropout_count = 0
results = []

for sample_number, reading in enumerate(sensor_readings, start=1):
    if reading is None:
        status = "DROPOUT"
        dropout_count += 1
        handled_value = last_valid_reading
        action = (
            "No previous valid reading available"
            if last_valid_reading is None
            else "Fallback to last valid reading"
        )

    elif (
        not isinstance(reading, (int, float))
        or not math.isfinite(reading)
        or not MIN_TEMPERATURE <= reading <= MAX_TEMPERATURE
    ):
        status = "FAULT"
        fault_count += 1
        handled_value = last_valid_reading
        action = (
            "Invalid reading; no fallback available"
            if last_valid_reading is None
            else "Invalid reading; fallback to last valid reading"
        )

    else:
        status = "VALID"
        valid_count += 1
        last_valid_reading = reading
        handled_value = reading
        action = "Accept sensor reading"

    results.append({
        "sample_number": sample_number,
        "raw_reading": reading,
        "status": status,
        "handled_value": handled_value,
        "action": action,
    })

with output_file.open("w", newline="") as file:
    fieldnames = [
        "sample_number",
        "raw_reading",
        "status",
        "handled_value",
        "action",
    ]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("Task-09: Fault & Dropout Handling")
print("---------------------------------")
print(f"Total samples: {len(sensor_readings)}")
print(f"Valid samples: {valid_count}")
print(f"Faulty samples: {fault_count}")
print(f"Dropout samples: {dropout_count}")
print(f"CSV output: {output_file}")
