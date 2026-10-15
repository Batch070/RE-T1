# Testing and Results — RE-T1 Spectra

**Project:** RE-T1 Spectra — Embedded AI and Sensor Processing  
**Document:** Testing and Results  
**Review date:** 16 October 2026  
**Environment:** Python virtual environment in GitHub Codespaces / Ubuntu  
**Purpose:** Document the testing approach, recorded benchmark measurements, sensor synchronization results, fault-handling results, and final verification requirements.

> **Evidence policy:** The numerical values in this document are previously recorded results. They should not be treated as proof that the current scripts have been rerun successfully. Before final submission, compare the values with the current output CSV files and record the actual verification status.

---

## 1. Testing Approach

Each task should be checked independently before final package integration. The objective is to verify that the implementation executes, produces the expected outputs, and behaves consistently with its documented purpose.

### 1.1 Pre-test checks

Before executing a task:

1. Navigate to the repository root.
2. Activate the intended Python virtual environment.
3. Check the Python interpreter version.
4. Confirm that the relevant script exists.
5. Confirm that required input files and output directories are available.
6. Check whether the script requires external packages.
7. Review the documented command and expected output filenames.

Example commands:

```bash
cd /workspaces/RE-T1

source .venv/bin/activate

python --version
python -m pip --version

git status --short
```

These commands verify the local environment and repository status. They do not, by themselves, establish that any task has passed its functional tests.

### 1.2 Execution checks

For each task:

- Run the documented script using the project's Python interpreter.
- Inspect terminal output for exceptions, warnings, and completion messages.
- Confirm the process exit status.
- Check that expected CSV files, plots, notebooks, or reports exist.
- Inspect output headers and representative records.
- Compare actual output with the documented expected behavior.
- Record any failure, unexpected value, or limitation.

Example:

```bash
python Task-10/mini_module.py
echo "Exit status: $?"
```

An exit status of `0` normally indicates that the process completed without reporting a command-level failure. It does not prove that every calculated result is correct; the generated output must also be inspected.

### 1.3 Output verification

For CSV-producing tasks, inspect the generated file:

```bash
head -n 10 Task-10/mini_module_results.csv
cat Task-11/performance_results.csv
```

Check the following:

- Column names are present and consistent.
- The number of records is plausible for the test configuration.
- Values use the expected units and data types.
- Faults, dropouts, and synchronization statuses are labelled correctly.
- Results correspond to the script and configuration used.
- Benchmark values in the report match the saved output from the same run.

For tasks that produce plots, confirm that the files open and represent the intended data. For notebooks, verify that the relevant cells execute in the documented environment.

### 1.4 Testing scope

The recorded demonstrations primarily establish software behavior using generated or synthetic data. They do not, by themselves, establish:

- Correctness with physical microphones or other real sensors.
- Robustness under real environmental noise.
- Real-time performance on the intended embedded hardware.
- Flight-control reliability or complete drone integration.
- Generalization accuracy of a trained AI model.

These distinctions must remain explicit in the final report.

---

## 2. Recorded Benchmark Results

### 2.1 Inference benchmark

The previously recorded CPU inference benchmark reported the following measurements.

| Metric | Recorded value |
|---|---:|
| Execution device | CPU |
| Average latency | 0.025377 ms |
| Median latency | 0.022693 ms |
| Minimum latency | 0.019887 ms |
| Maximum latency | 0.086772 ms |

These measurements describe one specific recorded benchmark run. They are not guaranteed deployment performance figures.

#### Interpretation

- **Average latency:** The arithmetic mean of the measured inference durations.
- **Median latency:** The middle measurement after sorting the measured durations.
- **Minimum latency:** The shortest observed duration in that run.
- **Maximum latency:** The longest observed duration in that run.

The difference between minimum and maximum latency illustrates that individual measurements varied during the benchmark.

The previously documented inference demonstration also reported a prediction and confidence value. These outputs demonstrate execution of the inference pipeline, but a confidence value alone does not establish model accuracy. The model's training status, evaluation dataset, and classification quality must be independently verified before drawing conclusions about predictive performance.

#### Verification procedure

Run the documented inference script and inspect the saved results:

```bash
python Task-04/inference_demo.py
cat Task-04/inference_results.csv
```

Confirm that the measured values correspond to the current run before publishing them as current results. If the script uses a different model, input, measurement procedure, or execution environment, record that difference.

**Limitation:** CPU timing from a development environment cannot be assumed to represent latency on the final embedded platform. Hardware, runtime configuration, model size, input preparation, and measurement overhead can all affect observed performance.

### 2.2 Timestamp search optimization

Task-11 compared linear nearest-timestamp search with binary-search-based timestamp lookup.

The following table contains the previously recorded results.

| Dataset size | Linear median (ms) | Binary median (ms) | Speedup |
|---:|---:|---:|---:|
| 100 | 0.908006 | 0.027421 | 33.114× |
| 500 | 24.405157 | 0.183162 | 133.244× |
| 1,000 | 94.519656 | 0.368016 | 256.836× |
| 2,000 | 387.312080 | 0.793937 | 487.837× |
| 4,000 | 1522.564064 | 2.545606 | 598.115× |

All five recorded comparisons reported matching outputs.

#### Method

The linear approach examines candidate timestamps sequentially until the relevant nearest timestamp is identified. Its search cost can increase with the number of candidate records.

The optimized approach uses binary search over sorted timestamps to narrow down the candidate position. This can reduce the number of comparisons needed to locate the relevant position.

For a sorted list of timestamps, binary search typically requires \(O(\log n)\) search operations, while a linear scan can require \(O(n)\) operations. The total runtime of the surrounding application may also depend on preprocessing, data access, matching logic, and other work.

#### Speedup calculation

The reported speedup is calculated as:

\[
\text{Speedup} =
\frac{\text{Linear median latency}}
{\text{Binary median latency}}
\]

For the 100-record case:

\[
\frac{0.908006}{0.027421}
\approx 33.114
\]

This means the recorded linear lookup took approximately 33.114 times as long as the binary lookup in that specific benchmark case.

#### Output correctness

The recorded tests reported matching outputs for all five dataset sizes. This supports the conclusion that the two methods returned equivalent results for the tested inputs.

It does not establish correctness for every possible timestamp arrangement. Additional testing should include duplicate timestamps, exact matches, queries outside the available range, empty inputs, and different timestamp distributions.

#### Verification procedure

```bash
python Task-11/performance_optimization.py
cat Task-11/performance_results.csv
```

Check that the CSV contains the expected dataset sizes and corresponding latency and speedup fields. The report should use values from the same saved run.

**Limitation:** Benchmark timings vary with machine load, runtime conditions, and measurement overhead. These measurements concern the isolated timestamp-search comparison and must not be presented as a benchmark of the entire sensor-processing or AI-inference system.

---

## 3. Sensor Synchronization — Task-08

### 3.1 Test configuration

The recorded Task-08 demonstration used:

- Three synthetic sensor streams.
- Twenty samples per sensor stream.
- A nominal sampling interval of 100 ms.
- A timestamp tolerance of 40 ms.
- One sensor stream as the reference timeline.
- Nearest-timestamp matching for the other streams.

The streams were generated for software testing rather than acquired from physical sensor hardware.

### 3.2 Recorded results

| Result | Recorded value |
|---|---:|
| Reference rows | 20 |
| Synchronized rows | 20 |
| Out-of-tolerance rows | 0 |
| Timestamp tolerance | 40 ms |

The recorded run matched all 20 reference rows and reported no out-of-tolerance rows.

### 3.3 Interpretation

The demonstration shows how multiple timestamped data streams can be matched against a reference timeline using a defined tolerance.

A synchronization status indicates whether the selected timestamp match satisfies the configured tolerance. It does not necessarily mean that all sensors were sampled simultaneously or that their physical clocks are perfectly synchronized.

### 3.4 Verification procedure

```bash
python Task-08/sensor_synchronization.py
head -n 10 Task-08/synchronized_data.csv
```

Verify that:

- The output file is present.
- The expected reference rows are represented.
- Timestamp differences and synchronization statuses are consistent with the configured tolerance.
- The report matches the current CSV contents.

### 3.5 Limitations

- The sensor values were synthetic.
- Nearest-timestamp matching does not correct clock drift.
- A selected sample may be reused for more than one reference timestamp, depending on the implementation.
- The recorded result does not establish synchronization accuracy with real sensors.
- More advanced applications may require interpolation, buffering, clock-offset estimation, drift correction, or missing-sample policies.

---

## 4. Fault and Dropout Handling — Task-09

### 4.1 Test configuration

The recorded Task-09 demonstration processed twelve synthetic samples. The test included valid measurements, deliberately invalid values, and missing measurements to exercise fault-detection and dropout-handling logic.

### 4.2 Recorded results

| Sample category | Recorded count |
|---|---:|
| Valid samples | 8 |
| Faulty samples | 2 |
| Dropout samples | 2 |
| **Total samples** | **12** |

The counts sum to twelve, consistent with the recorded test configuration.

### 4.3 Interpretation

The demonstration exercised three principal conditions:

1. **Valid sample:** A measurement that passes the configured validation checks.
2. **Faulty sample:** A measurement that violates the configured validation rules, such as an invalid sentinel value or a value outside the permitted range.
3. **Dropout sample:** A missing measurement, represented by a missing-value marker in the test input.

The implementation used a fallback based on the last valid measurement for handled invalid or missing values. This can allow a pipeline to continue processing, but it does not recover the true measurement that was unavailable.

### 4.4 Verification procedure

```bash
python Task-09/fault_dropout_handling.py
head -n 15 Task-09/fault_dropout_results.csv
```

Check that:

- Twelve input cases are represented in the recorded run.
- Valid, faulty, and dropout categories are labelled consistently.
- Invalid measurements are not silently treated as valid sensor readings.
- Fallback values and status fields agree with the implemented rules.
- The notes explain the configured valid range and sentinel values.

### 4.5 Limitations

- The test data were synthetic.
- The results do not establish the ability to detect every real sensor failure.
- Reusing the last valid measurement may produce stale values when a fault persists.
- The demonstration does not establish a safe response for every failure mode.
- Production use may require timeout thresholds, sensor-health metrics, stale-data indicators, fault severity levels, and explicit recovery policies.

---

## 5. Integrated Sensor Processing — Task-10

Task-10 combined the previously developed synchronization and sensor-validation concepts into a small demonstration pipeline.

### 5.1 Intended processing flow

The module integrates the following steps:

1. Generate synthetic sensor data.
2. Match sensor records against a reference timeline.
3. Evaluate timestamp differences against the configured tolerance.
4. Validate measurements against configured rules.
5. Identify faulty or missing measurements.
6. Apply the implemented fallback behavior.
7. Write processed results to a CSV file.

### 5.2 Previously recorded observations

The recorded demonstration reported:

| Observation | Recorded value |
|---|---:|
| Sensor streams | 3 |
| Samples per stream | 20 |
| Reference rows | 20 |
| Timestamp tolerance | 40 ms |
| Synchronized rows | 20 |
| Out-of-tolerance rows | 0 |
| Faults handled | 2 |
| Dropouts handled | 1 |

These values describe the previously recorded Task-10 execution. They should be checked against the current `mini_module_results.csv` before final acceptance.

### 5.3 Verification procedure

```bash
python Task-10/mini_module.py
head -n 15 Task-10/mini_module_results.csv
```

Inspect representative records for normal measurements, invalid values, and missing data. Confirm that the recorded status and handled value follow the implemented logic.

### 5.4 Limitations

The integrated demonstration uses synthetic data and does not prove physical sensor integration. Its behavior also depends on the timestamp-matching strategy and fallback rules. The report should not describe it as a complete flight-control system or as a fully validated real-time drone subsystem.

---

## 6. Validation Limitations

The recorded results must be interpreted within the scope of the experiments that produced them.

### 6.1 Synthetic inputs

Synthetic measurements and generated acoustic signals are useful for controlled, repeatable tests. They do not reproduce every characteristic of real sensors, including calibration errors, environmental interference, timing jitter, hardware faults, or changing operating conditions.

### 6.2 Environment-dependent measurements

Runtime measurements can vary with processor load, operating-system scheduling, runtime configuration, and measurement overhead. Benchmark figures should therefore include their test conditions and should not be presented as universal guarantees.

### 6.3 Algorithmic coverage

Matching outputs in a limited set of timestamp-search tests is evidence for those tested inputs only. Broader testing should cover edge cases and different data distributions.

Similarly, successful execution of fault-handling logic does not prove that all physical faults will be detected or safely handled.

### 6.4 Hardware and deployment validation

The recorded software demonstrations do not establish performance with physical microphones, production sensors, or the final embedded hardware. No claim of flight testing, real-world acoustic localization accuracy, or deployment readiness should be made without corresponding test evidence.

### 6.5 Model quality

A model that loads and returns a prediction has passed an execution check, not necessarily an accuracy or reliability evaluation. Claims about classification quality require a suitable evaluation dataset, defined metrics, and recorded evaluation results.

---

## 7. Final Verification Record

Complete this section using the actual final review. Do not fill in unknown values by assumption.

### 7.1 Environment record

| Field | Value |
|---|---|
| Verification date | __________________ |
| Operating system | __________________ |
| Python version | __________________ |
| Virtual environment | __________________ |
| Dependency file reviewed | Yes / No |
| Dependency installation tested | Yes / No / Not tested |

### 7.2 Execution record

| Task or component | Script executed | Output checked | Status / notes |
|---|---|---|---|
| Task-04 — Inference | __________ | __________ | __________ |
| Task-06 — Acoustic TDoA | __________ | __________ | __________ |
| Task-07 — Preprocessing | __________ | __________ | __________ |
| Task-08 — Synchronization | __________ | __________ | __________ |
| Task-09 — Fault handling | __________ | __________ | __________ |
| Task-10 — Integrated module | __________ | __________ | __________ |
| Task-11 — Optimization | __________ | __________ | __________ |
| Task-12 — Documentation | __________ | __________ | __________ |

Add entries for the remaining scheduled tasks if they are part of the final acceptance scope.

### 7.3 Output record

- [ ] Required CSV files are present and readable.
- [ ] CSV headers and representative records have been inspected.
- [ ] Required plots are present and open correctly.
- [ ] Required notebooks have been checked.
- [ ] Benchmark values match the saved results from the documented run.
- [ ] Task notes and final report agree with the implementation.
- [ ] Known limitations are documented.
- [ ] README setup and execution instructions have been reviewed.

### 7.4 Git and delivery record

| Field | Value |
|---|---|
| Repository | `RE-T1` |
| Intended branch | `main` |
| Final commit hash | __________________ |
| Push to intended remote verified | Yes / No |
| Local and remote commit hashes match | Yes / No |
| Working tree reviewed | Yes / No |
| Remaining issues | __________________ |

### 7.5 Final test status

- [ ] **Passed:** All required checks were executed and verified.
- [ ] **Passed with documented limitations:** Required checks passed, and known limitations are explicitly recorded.
- [ ] **Pending:** One or more checks still need to be performed.
- [ ] **Failed:** One or more required checks did not pass.

**Final conclusion:**

The recorded results demonstrate selected software behaviors for inference execution, timestamp-search optimization, sensor synchronization, fault/dropout handling, and integrated sensor processing. Final acceptance requires verification against the current scripts and output files, followed by review of the documentation and repository state.

The package should be declared complete only when the final verification record reflects actual execution and inspection, and the final commit hash and remote delivery status have been recorded.
