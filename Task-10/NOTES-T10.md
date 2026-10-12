# Task-10: Mini Module Assembly

## 1. Objective

The objective of this task is to integrate multiple sensor-processing functions into a single Python-based module. The module combines synthetic sensor data generation, timestamp synchronization, sensor data validation, fault detection, dropout detection, fallback handling, and CSV-based result reporting.

In embedded AI systems, individual processing components often perform separate operations. A complete system requires these components to work together in a defined sequence so that sensor data can be processed consistently and reliably.

This task demonstrates the integration of sensor synchronization and fault/dropout handling concepts into a unified workflow.

The main objectives are:

- To generate synthetic temperature, pressure, and humidity sensor streams.
- To use temperature timestamps as the reference for matching sensor readings.
- To identify the nearest timestamps from other sensor streams.
- To check timestamp differences against a configured tolerance.
- To validate sensor readings against predefined limits.
- To detect faulty and missing sensor values.
- To apply last-valid-reading fallback handling where possible.
- To generate a combined CSV report.
- To evaluate the integrated module using predefined test conditions.

## 2. Introduction

Mini Module Assembly is the process of combining multiple related software functions into a single integrated component.

In an embedded sensing system, multiple sensors may provide data at slightly different times. In addition, some sensor readings may be missing or invalid. If these conditions are not handled correctly, the resulting dataset may contain unreliable information.

Sensor synchronization helps associate readings from different sensor streams with a common reference time. Fault and dropout handling helps identify invalid or missing readings before they are trusted by downstream processing.

In this task, these concepts are combined into one Python program.

The program generates synthetic sensor data, matches readings using timestamps, checks synchronization tolerance, validates sensor values, records fallback values where available, and exports the results to a CSV file.

The implementation is a software demonstration. It does not directly communicate with physical sensors or execute a trained AI inference model.

## 3. System Requirements

### 3.1 Hardware Requirements

No physical sensor hardware is required.

The program generates synthetic sensor readings and executes on the development computer.

### 3.2 Software Requirements

- Python 3
- GitHub Codespaces or another Python development environment
- Python standard library
- A text editor or spreadsheet application for inspecting CSV output

### 3.3 Python Modules Used

The implementation uses the following standard-library modules:

| Module | Purpose |
|---|---|
| `csv` | Writes structured processing results to a CSV file. |
| `math` | Checks whether numeric sensor readings are finite. |
| `random` | Generates synthetic readings and timestamp jitter. |
| `pathlib` | Creates and manages output file paths. |

No third-party Python package is required.

## 4. System Configuration

The program uses the following configuration:

| Parameter | Value |
|---|---|
| Number of sensor streams | 3 |
| Sensor types | Temperature, pressure, humidity |
| Samples per sensor | 20 |
| Nominal sample interval | 100 ms |
| Synchronization tolerance | 40 ms |
| Reference sensor | Temperature |
| Output format | CSV |
| Output file | `Task-10/mini_module_results.csv` |

The sensor values and timing parameters are selected for demonstration purposes. They are not intended to represent the specifications of a particular physical sensor.

## 5. System Architecture

The integrated module follows this processing sequence:

**Synthetic Data Generation → Test Condition Injection → Timestamp Matching → Synchronization Check → Reading Validation → Fault/Dropout Handling → CSV Reporting**

### 5.1 Synthetic Data Generation

The program creates temperature, pressure, and humidity streams containing timestamped readings.

### 5.2 Test Condition Injection

Predefined invalid and missing values are inserted into the generated data to verify fault and dropout handling.

### 5.3 Timestamp Matching

Temperature timestamps are used as reference timestamps. The nearest pressure and humidity samples are selected for each reference row.

### 5.4 Synchronization Check

The maximum timestamp difference among the matched samples is compared with the configured 40 ms tolerance.

### 5.5 Reading Validation

Each matched sensor value is checked against its configured validation rules.

### 5.6 Fault and Dropout Handling

Faulty and missing readings are classified separately. The last valid value is recorded as the handled value when available.

### 5.7 CSV Reporting

The program writes the matched readings, validation statuses, handled values, timestamp differences, and synchronization status to a CSV file.

## 6. Synthetic Sensor Data Generation

The program generates three sensor streams:

- Temperature
- Pressure
- Humidity

Each stream contains 20 samples, resulting in 20 temperature-reference rows.

The nominal sampling interval is 100 milliseconds. The generated timestamps include small random variations to represent timing jitter. Each sensor stream also uses a different timestamp offset.

A fixed random seed is used to make the synthetic test data reproducible under the same code and compatible execution environment.

The sensor readings are illustrative values generated by Python. They are not collected from actual temperature, pressure, or humidity sensors.

## 7. Sensor Synchronization

### 7.1 Reference Sensor

The temperature stream is selected as the reference stream.

For every temperature sample, the program uses its timestamp as the reference timestamp against which the pressure and humidity timestamps are compared.

### 7.2 Nearest Timestamp Matching

The program searches each sensor stream for the sample with the smallest absolute timestamp difference from the reference timestamp.

The timestamp difference is calculated as:

**Time Difference = |Sensor Timestamp − Reference Timestamp|**

For example, if the reference timestamp is 100 ms and a pressure sample has a timestamp of 115 ms, the difference is:

**Time Difference = |115 − 100| = 15 ms**

This sample is a candidate for matching because its timestamp is close to the reference time.

### 7.3 Synchronization Tolerance

The configured synchronization tolerance is 40 milliseconds.

A reference row is marked `SYNCED` when all three matched timestamps are available and the maximum timestamp difference is no greater than 40 ms.

A row is marked `OUT_OF_TOLERANCE` when the required matching condition is not satisfied.

The tolerance determines whether the timestamps meet the program's configured timing requirement. It does not prove that physical sensor clocks are perfectly synchronized.

### 7.4 Independent Validation and Synchronization

Synchronization status and sensor validity status are different properties.

A row may be classified as `SYNCED` even if one of its readings is faulty or missing, provided the program can match the timestamps within tolerance.

Therefore, the synchronization result must be interpreted separately from the individual sensor validation results.

## 8. Sensor Fault and Dropout Handling

### 8.1 Fault Detection

A sensor reading is marked `FAULT` when it fails the program's validation checks.

The reading must be numeric, finite, and within the configured limits for that sensor.

The configured ranges are:

| Sensor | Minimum | Maximum |
|---|---:|---:|
| Temperature | 0 | 100 |
| Pressure | 80 | 120 |
| Humidity | 0 | 100 |

The program uses these limits as demonstration settings. The pressure unit is not specified in the implementation, so these limits should not be interpreted as a validated physical pressure specification.

The test data includes an invalid temperature value of `-999.0` and an invalid humidity value of `150.0`.

These values are outside the configured limits and are classified as faulty.

### 8.2 Dropout Detection

A sensor reading represented by `None` is marked `DROPOUT`.

The test data includes a missing pressure sample.

When the program encounters this sample, it increments the dropout counter and records the missing reading in the output.

The current implementation explicitly inserts a missing value into the synthetic data. It does not independently detect an actual sensor disconnection or communication timeout.

### 8.3 Valid Reading Handling

A reading is marked `VALID` if it is numeric, finite, and within the configured limits.

The program accepts the reading and stores it as the latest valid value for that sensor.

This value can be used by the fallback logic if a later sample is faulty or missing.

### 8.4 Fallback Handling

When a reading is faulty or missing, the program records the last valid value for that sensor if one is available.

For example, if the last accepted temperature reading is 24.17 and the next temperature sample contains an invalid value, the raw invalid value remains in the output while 24.17 is recorded as the handled value.

The program keeps the raw reading and handled value in separate columns so that the original data remains available for analysis.

A fallback value is a reused measurement, not a new sensor measurement. The implementation does not check how old the fallback value is.

## 9. Implementation Details

The program is organized into separate functions.

### 9.1 `generate_sensor_stream()`

This function generates timestamped synthetic readings for a sensor.

It uses the configured sample count, nominal sampling interval, sensor-specific timestamp offset, and random jitter.

### 9.2 `inject_test_conditions()`

This function inserts predefined fault and dropout test cases into the generated streams.

It creates:
- One invalid temperature value.
- One missing pressure value.
- One invalid humidity value.

### 9.3 `find_nearest()`

This function searches a sensor stream and returns the sample whose timestamp has the smallest absolute difference from the reference timestamp.

### 9.4 `validate_reading()`

This function checks whether a reading is missing, numeric, finite, and within the configured limits.

It returns one of the following statuses:

- `VALID`
- `FAULT`
- `DROPOUT`

### 9.5 `main()`

The main function coordinates the complete module.

Its responsibilities include:

1. Generating the sensor streams.
2. Injecting predefined test conditions.
3. Selecting reference timestamps.
4. Matching pressure and humidity samples.
5. Calculating timestamp differences.
6. Validating individual sensor readings.
7. Applying fallback handling.
8. Counting synchronization results, faults, and dropouts.
9. Writing the results to the CSV file.
10. Printing the execution summary.

## 10. CSV Output Structure

The generated output file is:

`Task-10/mini_module_results.csv`

The CSV contains the following columns:

| Column | Description |
|---|---|
| `sample_number` | Sequential reference row number. |
| `reference_timestamp_ms` | Timestamp of the temperature reference sample. |
| `temperature_timestamp_ms` | Matched temperature timestamp. |
| `temperature_raw` | Original temperature reading. |
| `temperature_status` | Temperature validation result. |
| `temperature_handled` | Accepted or fallback temperature value. |
| `pressure_timestamp_ms` | Matched pressure timestamp. |
| `pressure_raw` | Original pressure reading. |
| `pressure_status` | Pressure validation result. |
| `pressure_handled` | Accepted or fallback pressure value. |
| `humidity_timestamp_ms` | Matched humidity timestamp. |
| `humidity_raw` | Original humidity reading. |
| `humidity_status` | Humidity validation result. |
| `humidity_handled` | Accepted or fallback humidity value. |
| `max_timestamp_difference_ms` | Maximum timestamp difference among matched samples. |
| `sync_status` | Overall timing status for the reference row. |

The CSV format makes the output easy to inspect using a text editor, spreadsheet application, or Python data-analysis tools.

## 11. Execution Procedure

The program is executed from the repository root using:

`python Task-10/mini_module.py`

After execution, the program prints the sensor count, sample count, synchronization tolerance, synchronization summary, fault count, dropout count, and output file path.

The CSV file can be inspected using:

`head -n 10 Task-10/mini_module_results.csv`

The generated results should be checked to confirm that the expected columns are present and that invalid and missing values are