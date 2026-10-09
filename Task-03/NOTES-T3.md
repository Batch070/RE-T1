# Task-03: Sensor Data Ingestion

## Project information

- **Project:** RudraEdge RE-T1 (Spectra)
- **Engineer:** Ashish Thakur
- **Role:** Embedded AI Engineer
- **Task order reference:** `REA/2026/RE-T1/TRAIN-001`
- **Assigned date:** 07 October 2026
- **Required output:** Sensor ingestion demo
- **Execution environment:** GitHub Codespaces, Ubuntu Linux
- **Personal expenditure:** ₹0

## 1. Task objective

The goal was to build a small, repeatable demonstration of a sensor-data ingestion pipeline. It generates synthetic sensor packets, preserves the raw input, parses the packet fields, validates the contents, and writes valid and rejected records to separate CSV files.

The task uses synthetic data, so no physical sensors or hardware procurement are needed.

## 2. Why sensor ingestion matters

A sensor-processing or AI system cannot safely use data until it has been received, interpreted and checked. Data ingestion is the entry point between a sensor or upstream producer and later processing stages.

A robust ingestion stage should help answer:

- Which sensor produced this record?
- When was the record generated?
- What kind of measurement does it contain?
- Is the value numeric and usable?
- Are required fields missing?
- Is the sensor identifier recognized?
- Should the record be accepted or rejected?

Keeping rejected data separate helps make data-quality problems visible instead of silently passing malformed input downstream.

## 3. Pipeline architecture

```text
Synthetic sensor packet generator
              |
              v
       Raw packets CSV
              |
              v
      Parse packet fields
              |
              v
       Validate each packet
              |
       +------+------+
       |             |
       v             v
 Valid packet     Invalid packet
       |             |
       v             v
 valid CSV       rejected CSV
```

## 4. Concepts studied

### 4.1 Raw sensor packet

A raw packet is the input representation received by the ingestion stage. In this demonstration, packet fields include sensor identification, timestamp, type, measurement value, unit and status.

### 4.2 Parsing

Parsing converts a raw packet into structured fields that code can inspect individually. Parsing must account for missing fields and malformed input rather than assuming every packet is well-formed.

### 4.3 Validation

Validation checks whether a parsed record satisfies the requirements expected by the application. This demo checks items such as:

- Required field count
- Recognized sensor ID
- Expected sensor type and unit
- Valid timestamp
- Numeric measurement value
- Status field

Validation rules are specific to the demonstration schema. A production system would need documented sensor ranges, units, timestamp rules and error policies.

### 4.4 Rejected records

A rejected record fails one or more validation rules. Retaining rejected records in a separate output makes failures auditable and helps debug ingestion logic.

### 4.5 Deterministic synthetic data

The generator uses `random.seed(42)`. This makes the pseudo-random sequence repeatable so test runs can be compared consistently.

## 5. Implementation details

The Python demo performs these steps:

1. Generate synthetic packets for temperature, pressure, humidity and acceleration sensors.
2. Use a fixed random seed so the generated data is repeatable.
3. Save the original generated packets to a raw CSV file.
4. Parse each packet into structured fields.
5. Check the required field count and validate the fields.
6. Route accepted records to the valid-data collection.
7. Route invalid records to the rejected-data collection.
8. Write the three collections to their corresponding CSV outputs.

### Deliberately invalid test cases

The demonstration includes three intentional failure cases:

1. A non-numeric sensor value (`ABC`).
2. A packet with a missing field.
3. An unknown sensor ID.

These cases test whether the pipeline rejects malformed or unrecognized input instead of accepting it as valid.

## 6. Recorded test result

The recorded run generated **23 packets**:

| Category | Count |
|---|---:|
| Total packets | 23 |
| Valid packets | 20 |
| Rejected packets | 3 |

These counts describe the recorded demo run. If the generator or validation logic changes, rerun the script and inspect the new output before reusing these figures.

## 7. Tools and libraries

- Python 3
- Standard-library `csv`
- Standard-library `random`
- Standard-library `datetime`
- Standard-library `pathlib`
- Bash/Linux CLI
- Git and GitHub Codespaces

No external AI service or physical sensor was needed for this task.

## 8. Repository outputs

After task-wise folder organization:

```text
Task-03/
├── sensor_ingestion_demo.py
├── raw_sensor_data.csv
├── valid_sensor_data.csv
├── rejected_sensor_data.csv
└── NOTES.md
```

The files were originally developed under `sensor_ingestion/` and then moved into `Task-03/`.

Initial implementation commit: `5a1d703`, pushed to GitHub before the later folder reorganization.

## 9. Testing and run instructions

From the repository root:

```bash
python -m py_compile Task-03/sensor_ingestion_demo.py
python Task-03/sensor_ingestion_demo.py
```

Inspect the outputs:

```bash
head Task-03/raw_sensor_data.csv
head Task-03/valid_sensor_data.csv
cat Task-03/rejected_sensor_data.csv
```

Check the total number of data rows (excluding each header) if you need to verify a new run.

## 10. Observation: repeated output

**Observation:** Running the script again produced the same synthetic values.

**Explanation:** The generator uses `random.seed(42)`, which intentionally fixes the pseudo-random sequence.

**Recommended practice:** Keep the fixed seed for reproducible tests. Change or remove it only when varying data is specifically required and document that change.

The CSV files are opened in write mode, so each run replaces previous output files instead of appending new records. Preserve prior runs separately if historical comparison is required.

## 11. Engineering limitations

- The records are synthetic and do not prove behavior with physical sensors.
- Validation rules cover only the fields and checks implemented in this demo.
- Real devices may require handling packet loss, duplicate timestamps, out-of-range values, corrupted bytes and asynchronous arrivals.
- The raw, valid and rejected CSV files are useful for this small demonstration, but larger systems may need structured logs, schema versioning and durable storage.

## 12. Outcome

A repeatable ingestion demo was implemented. It generated raw synthetic packets, parsed and validated them, and separated the recorded 20 valid packets from 3 intentionally invalid packets.

## 13. Next assigned task

**Task-04 — Embedded AI Inference:** use local/open-source tools to run a basic model inference and save its output.
