# Task-08: Sensor Synchronization

**Engineer:** Ashish Thakur  
**Role:** Embedded AI Engineer  
**Task Date:** 12 October 2026  
**Project:** RudraEdge RE-T1 (Spectra)  
**Task Category:** Sensor Synchronization

---

## 1. Objective

The objective of this task is to demonstrate sensor timestamp synchronization using Python and synthetic sensor data.

In a multi-sensor embedded system, different sensors may produce readings at slightly different times. If these readings are processed together without checking their timestamps, the system may combine measurements that do not represent approximately the same point in time.

This task implements a basic timestamp-alignment workflow for three simulated sensors: temperature, pressure, and humidity.

The implementation aims to:
- Generate synthetic readings with timestamps.
- Simulate timestamp offsets and small timing variations.
- Select the nearest reading for each reference timestamp.
- Apply a maximum allowed timestamp difference.
- Label rows as synchronized or out of tolerance.
- Export the aligned records to a CSV file.

No physical sensors or external hardware are used.

## 2. Background and Theory

### 2.1 Sensor Timestamps

A timestamp records when a sensor measurement is associated with a point in time.

For example, a temperature reading may have a timestamp of 10:00:00.005, while a pressure reading may have a timestamp of 10:00:00.018.

The difference between these timestamps is 13 milliseconds.

When readings from multiple sensors are combined, their timestamps should be checked so that the measurements are sufficiently close in time for the intended application.

### 2.2 Sampling Interval

The nominal sampling interval is the expected time between consecutive samples.

The implementation uses a nominal interval of 100 milliseconds.

Sampling frequency is the reciprocal of the sampling interval:

    Sampling frequency = 1 / Sampling interval

For a 100 ms interval:

    Sampling frequency = 1 / 0.1 seconds
                       = 10 Hz

This is the nominal rate configured for the synthetic streams, not a measurement of physical sensor performance.

### 2.3 Timestamp Offset and Jitter

A timestamp offset is a difference between the timing of one sensor stream and the reference stream.

Jitter refers to small variations in the timing of successive readings.

To demonstrate these effects, the synthetic data generator applies configured offsets and random timing variations to the generated timestamps.

A fixed random seed makes the experiment reproducible under the same execution conditions.

### 2.4 Nearest-Timestamp Matching

The implementation uses temperature timestamps as the reference timeline.

For every temperature timestamp, the program searches each sensor stream and selects the reading with the smallest absolute timestamp difference.

The timestamp difference is calculated as:

    Difference = absolute(sensor timestamp - reference timestamp)

The maximum allowed difference is configured as 40 milliseconds.

A row is marked SYNCED only when the selected readings from all three streams are within the configured tolerance of the reference timestamp. Otherwise, it is marked OUT_OF_TOLERANCE.

The method is a simple nearest-neighbor approach. It does not perform interpolation or correct the underlying clocks of the sensors.

## 3. Implementation

The implementation is contained in:

    Task-08/sensor_synchronization.py

The program performs the following operations:

1. Imports the Python standard-library modules required for CSV output, timestamps, file paths, and reproducible random data.
2. Configures a reference start time of 12 October 2026 at 10:00:00.
3. Generates 20 synthetic readings for each of three sensors.
4. Uses a nominal sample interval of 100 milliseconds.
5. Applies sensor-specific timestamp offsets and small random timing variations.
6. Uses the temperature stream as the reference timeline.
7. Finds the nearest reading in each stream for every reference timestamp.
8. Compares timestamp differences against the 40 ms tolerance.
9. Labels each output row as SYNCED or OUT_OF_TOLERANCE.
10. Writes the resulting records to a CSV file and prints a summary.

## 4. Configuration

| Parameter | Configured value |
|---|---|
| Number of sensor streams | 3 |
| Sensors | Temperature, pressure, humidity |
| Samples per stream | 20 |
| Nominal sample interval | 100 ms |
| Nominal sampling rate | 10 Hz |
| Maximum allowed timestamp difference | 40 ms |
| Reference stream | Temperature |
| Data source | Synthetic |
| Output format | CSV |

## 5. Execution Results

The program was executed in the project's Python virtual environment in GitHub Codespaces.

Observed terminal output:

- Sensors: 3
- Samples per sensor: 20
- Nominal sample interval: 100 ms
- Maximum allowed difference: 40 ms
- Reference rows: 20
- Synchronized rows: 20
- Out-of-tolerance rows: 0

The program completed successfully and generated the output CSV.

These counts describe the particular synthetic test run. They do not establish real-world sensor synchronization accuracy.

## 6. Output File

### synchronized_data.csv

Path:

    Task-08/synchronized_data.csv

The CSV contains the following columns:

- reference_timestamp: Timestamp selected from the temperature stream as the reference.
- temperature: Selected temperature value.
- temperature_timestamp: Timestamp of the selected temperature reading.
- pressure: Selected pressure value.
- pressure_timestamp: Timestamp of the selected pressure reading.
- humidity: Selected humidity value.
- humidity_timestamp: Timestamp of the selected humidity reading.
- status: Synchronization status based on the configured tolerance.

The output can be inspected using a text editor, spreadsheet application, or Python CSV-processing tools.

## 7. Tools and Libraries

- Python
- Python standard-library modules: csv, random, datetime, pathlib
- Python virtual environment (.venv)
- Bash/Linux command-line interface
- Git and GitHub Codespaces

No additional third-party Python package is required for this script.

## 8. Limitations

- All readings are synthetic; no physical sensor was connected.
- The temperature stream is used as the reference timeline.
- The nearest reading is selected independently for each reference timestamp.
- The method does not estimate or correct clock drift.
- The method does not use interpolation to estimate values at a common time.
- It does not explicitly prevent the same source reading from being selected for multiple reference timestamps.
- The tolerance is fixed at 40 milliseconds and may not be appropriate for every application.
- The successful synthetic run does not demonstrate real hardware synchronization accuracy or end-to-end latency.

## 9. Possible Improvements

Future improvements could include:

- Testing with recorded sensor timestamps.
- Comparing different synchronization tolerances.
- Adding missing-sample and delayed-sample scenarios.
- Preventing duplicate source-sample assignments when required.
- Implementing interpolation for continuous sensor signals.
- Estimating clock offset and drift.
- Reporting the maximum, minimum, and average timestamp differences.
- Testing whether the synchronization method meets the timing requirements of the target embedded application.

## 10. Conclusion

Task-08 demonstrates a basic sensor synchronization workflow using Python and synthetic data.

Three sensor streams were generated with timestamp offsets and timing variations. The program used the temperature timestamps as a reference, selected the nearest readings from the sensor streams, applied a 40 ms tolerance, and exported the aligned records to CSV.

In the observed run, all 20 reference rows were classified as synchronized. The implementation provides a starting point for understanding timestamp alignment, while further testing with real sensor data would be required to validate an actual embedded system.

## 11. Expenditure

Total expenditure: ₹0.

The task used the existing development environment and Python standard library. No additional hardware or paid software was required.
