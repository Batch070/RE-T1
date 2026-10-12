# Task-09: Fault & Dropout Handling

## 1. Objective

The main objective of this task is to develop a Python-based sensor monitoring system that can identify invalid sensor readings and missing sensor samples. The system demonstrates basic fault detection, dropout detection, data validation, and fallback handling.

In embedded systems, sensors continuously provide data to a controller or an AI processing unit. However, sensor readings may sometimes be invalid, missing, or outside the expected operating range. If such readings are processed without validation, they may affect system reliability and lead to incorrect decisions.

This task demonstrates how a monitoring program can identify problematic readings, classify them according to their status, and record the results for further analysis.

The specific objectives are:

- To simulate sensor readings using Python.
- To identify valid and invalid temperature values.
- To detect missing sensor samples.
- To distinguish sensor faults from sensor dropouts.
- To implement fallback handling using the last valid reading.
- To generate a CSV report containing the processing results.
- To evaluate the behavior of the system using predefined test data.

## 2. Introduction

Fault and dropout handling is an important part of reliable embedded systems. Embedded devices frequently depend on sensor measurements to monitor environmental conditions, machinery, vehicles, and other physical systems.

A sensor may produce an incorrect value because of hardware problems, electrical interference, communication errors, or measurement limitations. Similarly, a sensor may stop providing data temporarily because of a communication failure, a disconnected cable, or a device malfunction.

A monitoring system should not blindly accept every incoming value. It should validate the readings, identify abnormal conditions, and decide how to handle them.

In this task, a synthetic temperature dataset is used to demonstrate these situations. The dataset contains normal readings, invalid temperature values, and missing samples. The Python program processes each sample and assigns one of three statuses:

- `VALID`
- `FAULT`
- `DROPOUT`

The processed results are saved in a CSV file for inspection and documentation.

## 3. Basic Concepts

### 3.1 Sensor Fault

A sensor fault occurs when a sensor provides a reading that fails a defined validation rule.

For example, if a temperature monitoring application uses a configured acceptable range of 0°C to 100°C, readings such as -999°C or 150°C will be classified as invalid by this demonstration.

A fault may be caused by several factors:

- Sensor hardware malfunction.
- Electrical noise or interference.
- Incorrect data conversion.
- Communication or parsing errors.
- Sensor readings outside the configured acceptable range.

The program does not determine the physical cause of a fault. It only detects that a reading violates its validation rules.

### 3.2 Sensor Dropout

A sensor dropout occurs when an expected sensor sample is missing.

For example, a monitoring system may expect a new temperature reading, but no value is available for that sample.

In this task, Python's `None` value represents a missing reading.

Possible real-world causes of dropout include:

- Temporary communication failure.
- Sensor disconnection.
- Missed data packets.
- Sensor power interruption.
- Failure of the data acquisition process.

The current implementation simulates missing samples rather than detecting an actual hardware timeout.

### 3.3 Difference Between Fault and Dropout

| Sensor Fault | Sensor Dropout |
|---|---|
| A reading is received but fails validation. | An expected reading is missing. |
| Example: -999°C when the configured range is 0–100°C. | Example: no temperature value is available. |
| The program marks the sample as `FAULT`. | The program marks the sample as `DROPOUT`. |
| The raw value is retained for reporting. | The missing value is represented by `None` in the input. |

### 3.4 Data Validation

Data validation is the process of checking whether a sensor reading satisfies predefined rules before accepting it.

In this task, the configured temperature limits are:

- Minimum temperature: 0°C
- Maximum temperature: 100°C

A numeric reading is accepted only if it is finite and lies within this range.

The validation rule is:

Valid reading = finite numeric value AND 0 ≤ reading ≤ 100

For example:

- 25.2°C: Valid
- 26.8°C: Valid
- -999°C: Invalid
- 150°C: Invalid
- `None`: Missing sample

These limits are demonstration settings and should not be treated as universal temperature limits for every sensor or application.

## 4. System Design and Working Principle

The program follows a simple data-processing workflow.

### Step 1: Configure the System

The program defines the acceptable temperature range and prepares a predefined list of synthetic sensor readings.

The list includes normal temperature values, invalid numeric values, and missing samples.

### Step 2: Read Each Sample

The program processes the readings one by one. Every sample is assigned a sequential sample number so that its status can be traced in the output file.

### Step 3: Check for Dropout

If the reading is `None`, the program identifies it as a dropout.

The dropout counter is incremented. If an earlier valid reading exists, that reading is recorded as the fallback value.

### Step 4: Check for Fault

If the reading is present, the program checks whether it is numeric, finite, and within the configured temperature limits.

A value that fails these checks is classified as a fault. The fault counter is incremented, and the last valid reading is recorded as the fallback value when available.

### Step 5: Accept Valid Data

If the reading passes validation, it is marked as `VALID`.

The valid counter is incremented, and the current reading becomes the last valid reading for subsequent fallback operations.

### Step 6: Generate the Output

The program records the sample number, raw reading, status, handled value, and handling action.

After all samples have been processed, the results are exported to a CSV file.

## 5. Implementation Details

### 5.1 Configuration

The program uses two configuration constants:

- `MIN_TEMPERATURE = 0.0`
- `MAX_TEMPERATURE = 100.0`

These constants define the acceptable temperature range used by the validation logic.

Keeping the limits in configuration variables makes it easier to adapt the demonstration to a different sensor range.

### 5.2 Synthetic Input Data

The program uses a predefined list of 12 samples.

The list contains:
- Eight valid temperature readings.
- Two invalid numeric readings.
- Two missing readings represented by `None`.

The invalid test values are -999°C and 150°C.

Using predefined data makes the experiment reproducible because the same input sequence can be processed repeatedly.

### 5.3 Fault Detection Logic

The program checks whether a reading is numeric, finite, and within the configured range.

The `math.isfinite()` function helps reject special numeric values such as NaN and positive or negative infinity.

The range check rejects values below the minimum or above the maximum.

A reading that fails these checks receives the `FAULT` status.

### 5.4 Dropout Detection Logic

The program treats `None` as an explicit missing sample.

When this condition is detected, the sample receives the `DROPOUT` status.

This approach is suitable for demonstrating missing-value handling. In an actual sensor system, dropout detection may require timestamps, expected sampling intervals, and timeout monitoring.

### 5.5 Fallback Handling

Fallback handling uses the last valid reading when the current sample is missing or invalid, provided that a previous valid reading is available.

For example, if the last accepted temperature is 25.7°C and the next sample is missing, the program records 25.7°C as the handled value.

The original reading is not replaced in the raw input field. The CSV preserves both the raw reading and the handled value.

This distinction is useful for debugging and analysis.

However, a previous reading may become outdated. Fallback handling therefore demonstrates a basic recovery strategy rather than guaranteeing an accurate current temperature.

### 5.6 Counters and Summary

The program maintains counters for:

- Total samples.
- Valid samples.
- Faulty samples.
- Dropout samples.

These counters provide a summary of the dataset and help verify that the classification process has completed.

### 5.7 CSV Reporting

The program writes its results to:

`Task-09/fault_dropout_results.csv`

The CSV contains the following columns:

| Column | Description |
|---|---|
| `sample_number` | Sequential number of the input sample. |
| `raw_reading` | Original sensor value or missing-value representation. |
| `status` | Classification as `VALID`, `FAULT`, or `DROPOUT`. |
| `handled_value` | Accepted reading or fallback value, when available. |
| `action` | Description of the action taken by the program. |

CSV reporting allows the results to be inspected using a text editor, spreadsheet application, or Python data-analysis tools.

## 6. Experimental Results

The program was executed successfully using the predefined synthetic dataset.

The observed summary was:

| Metric | Result |
|---|---:|
| Total samples | 12 |
| Valid samples | 8 |
| Faulty samples | 2 |
| Dropout samples | 2 |

The counts satisfy the following check:

Total samples = Valid samples + Faulty samples + Dropout samples

12 = 8 + 2 + 2

This confirms that all 12 input samples were classified into the three configured categories.

The generated CSV file provides the individual sample-level results.

The results demonstrate the program's basic classification and reporting behavior. They do not establish the detection accuracy of a physical sensor because the input data is synthetic and the fault cases are predefined.

## 7. Tools and Technologies Used

The task uses:

- Python 3 for implementing the monitoring logic.
- `csv` for writing structured results.
- `math` for checking finite numeric values.
- `pathlib` for constructing the output file path.
- GitHub Codespaces as the development environment.
- CSV format for storing the results.

All required Python modules belong to the Python standard library. No third-party Python package is required for this implementation.

## 8. Limitations

The current implementation demonstrates basic fault and dropout handling but has several limitations.

### 8.1 Synthetic Data

The input values are generated in the program rather than collected from a physical sensor.

### 8.2 Explicit Missing-Value Detection

Dropouts are represented by `None`. The program does not independently detect a disconnected sensor or a missing network packet.

### 8.3 No Communication Timeout

The implementation does not monitor real-time arrival timestamps or trigger a timeout when a reading is delayed.

### 8.4 No Physical Fault Diagnosis

The program identifies readings that fail configured checks but cannot determine whether the cause is a sensor defect, wiring problem, or environmental condition.

### 8.5 Possible Stale Fallback Data

The last valid reading may no longer represent the current temperature. The implementation does not enforce a maximum age for fallback data.

### 8.6 No Automatic Hardware Recovery

The program does not reconnect a sensor, reset a device, or restart a data acquisition service.

### 8.7 Fixed Validation Range

The temperature range is hard-coded for this demonstration. A real system would require limits based on sensor specifications and application requirements.

## 9. Future Improvements

The implementation can be extended in several ways.

### 9.1 Real Sensor Integration

Connect a physical sensor or a real data stream to test the monitoring logic with actual measurements.

### 9.2 Timeout-Based Dropout Detection

Record sample arrival timestamps and mark a sensor as unavailable when no new reading arrives within the configured timeout.

### 9.3 Stale-Data Checks

Associate each fallback value with its original timestamp and reject it when its age exceeds an acceptable limit.

### 9.4 Fault Logging and Alerts

Record the time, sensor identifier, fault category, and recovery action. Important faults could trigger an alert.

### 9.5 Recovery Mechanisms

Introduce controlled retry logic, sensor reconnection, or data acquisition restart procedures where supported by the hardware.

### 9.6 Configurable Sensor Limits

Move sensor-specific validation ranges into a configuration file so that the system can support multiple sensor types.

### 9.7 Multi-Sensor Fault Handling

Extend the program to monitor multiple sensor streams and distinguish individual sensor failures from system-wide failures.

### 9.8 Testing and Evaluation

Add automated tests for valid readings, out-of-range values, missing samples, NaN, infinity, and situations where no previous valid reading is available.

## 10. Safety and Reliability Considerations

Fault handling should prevent invalid data from being silently treated as trustworthy data.

A fallback value should be identified as an estimated or reused value rather than a fresh measurement. Systems that depend on safety-critical sensor readings may need to reject stale data, enter a safe operating state, or request human intervention.

The correct response depends on the system's requirements. Reusing a previous value is not always safe, especially when the measured quantity changes rapidly.

## 11. Conclusion

Task-09 successfully demonstrates a basic Python-based fault and dropout handling workflow using synthetic temperature sensor data.

The program validates readings against a configured range, identifies invalid values and missing samples, maintains counters, applies last-valid-reading fallback where available, and exports sample-level results to a CSV file.

The experiment processed 12 samples, classifying eight as valid, two as faulty, and two as dropouts.

The implementation provides a foundation for further development of reliable embedded sensor-monitoring systems. Real sensor integration, timeout-based dropout detection, stale-data validation, and recovery mechanisms remain future improvements.