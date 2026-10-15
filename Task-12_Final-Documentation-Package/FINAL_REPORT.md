# RE-T1 (SPECTRA) — Final Technical Report

**Project:** Rudra Edge RE-T1 (Spectra)  
**Organization:** RudraEdge Aerospace  
**Engineer:** Ashish Thakur  
**Role:** Embedded AI Engineer  
**Task Order Reference:** `REA/2026/RE-T1/TRAIN-001`  
**Reporting Date:** 16 October 2026  
**Repository:** https://github.com/Batch070/RE-T1  
**Development Environment:** GitHub Codespaces, Ubuntu Linux, Python virtual environment (`.venv`)

---

## 1. Project Overview

RE-T1 (Spectra) is an embedded-AI and sensor-processing development project focused on system monitoring, sensor-data handling, acoustic signal processing, timestamp synchronization, fault/dropout handling, inference experimentation, and performance optimization.

The work was organized as a sequence of engineering tasks, each addressing one part of the software workflow. Python was used for demonstrations and data processing, CSV files were used to store selected results, Markdown files were used for technical notes, and Git/GitHub supported version control.

Several demonstrations used synthetic datasets because physical sensors or target hardware were not available for those experiments. Synthetic data allows a repeatable test of code paths, algorithms, and output generation. It does not establish real-world sensor accuracy, real-time behavior, or reliable operation on a drone. This distinction is maintained throughout the report.

The project work should be understood as development of software building blocks that may contribute to an onboard data-processing or intelligence subsystem. It is not, by itself, evidence that a complete drone brain, flight controller, or flight-ready system has been implemented or validated.

## 2. Project Objectives

The main objectives of the task sequence were:

1. Understand the system architecture, repository layout, task sequence, and development environment.
2. Monitor operating-system resources and record selected measurements.
3. Develop a sensor-data ingestion demonstration and organize readings for downstream processing.
4. Execute a small AI inference demonstration and record its output.
5. Benchmark inference latency using repeated measurements.
6. Explore acoustic signal processing and Time Difference of Arrival (TDoA) through correlation.
7. Apply basic acoustic preprocessing, smoothing, and segmentation.
8. Synchronize timestamped sensor streams against a reference timeline.
9. Detect invalid readings and missing sensor samples.
10. Test a last-valid-value fallback policy for fault/dropout cases.
11. Integrate sensor synchronization and fault/dropout handling in a mini module.
12. Compare linear and binary-search-based timestamp lookup approaches.
13. Record results, assumptions, limitations, dependencies, and reproducibility steps.
14. Prepare a final documentation package for technical review and handover.

## 3. Scope and Engineering Approach

### 3.1 Scope

The work described in this report covers software demonstrations and their associated notes or output files. It includes:

- Linux resource monitoring
- Sensor-style data ingestion
- A small AI inference demonstration
- Inference latency benchmarking
- Synthetic acoustic signal generation and cross-correlation
- Acoustic signal smoothing and segmentation
- Timestamp-based sensor synchronization
- Invalid-value and missing-sample handling
- Integration of selected processing steps
- Timestamp-search performance comparison
- Final technical documentation and package checks

### 3.2 Engineering approach

The tasks were developed incrementally. Each task focused on a specific concept before later tasks combined some of those concepts. Scripts were executed in the project environment, and generated CSV files or plots were inspected where available. Results are reported with the configuration and limitations known from the recorded work.

### 3.3 Evidence levels

The report distinguishes three types of evidence:

- **Recorded software result:** A script produced a result or file in the development environment.
- **Synthetic-data demonstration:** The algorithm was exercised using generated data rather than physical sensor measurements.
- **Hardware validation:** Testing with the intended physical sensor or embedded target. Such validation is not established by the synthetic demonstrations described here.

## 4. Development Environment and Tools

### 4.1 Environment

- Operating environment: Linux-based GitHub Codespaces
- Distribution observed in the development environment: Ubuntu Linux
- Programming language: Python
- Virtual environment: `.venv`
- Version control: Git and GitHub
- Command-line interface: Bash/Linux CLI
- Data and documentation formats: CSV and Markdown
- Plotting: Matplotlib where used

### 4.2 Python modules and libraries

The task scripts use Python standard-library modules, including:

- `csv` — read and write CSV result files.
- `pathlib` and `os` — handle paths and file-system operations.
- `datetime` — work with timestamps.
- `random` and `math` — generate synthetic data and perform numerical calculations.
- `time` — measure elapsed execution time.
- `statistics` — summarize repeated timing measurements.
- `bisect` — perform binary-search-based operations on sorted timestamp data.

Other project demonstrations use packages such as NumPy, Matplotlib, psutil, and PyTorch. The exact dependencies required by each script should be confirmed from the script imports and the actual environment. A `requirements.txt` generated from an environment may contain transitive or unrelated packages, so it should be reviewed before being treated as a minimal and portable dependency list.

### 4.3 General setup and verification commands

From the repository root:

```bash
cd /workspaces/RE-T1
source .venv/bin/activate
pwd
which python
python --version
git status --short --branch
```

If a file or folder is not found, inspect the actual repository tree before assuming a command succeeded:

```bash
find . -maxdepth 2 -type f | sort
```

## 5. Detailed Task Execution Summary

### 5.1 Task-01 — Architecture Orientation (5 October)

**Purpose:** Understand the project structure, system context, components, task sequence, and expected engineering workflow.

**Work performed:** Reviewed the architecture and created or maintained orientation documentation describing the initial project understanding.

**Why it matters:** An engineer needs to understand where each software component belongs, what data it consumes, what output it produces, and how later tasks relate to the overall system.

**Outcome:** Architecture-orientation notes were included in the task repository.

**Limitations:** Architecture documentation records the intended or understood structure. It does not prove that all described components exist as physical hardware or that the complete system has been integrated.

### 5.2 Task-02 — Linux Systems and Monitoring (6 October)

**Purpose:** Become familiar with the Linux development environment and basic resource monitoring.

**Work performed:** Used a Python monitoring script to collect selected system-resource measurements and record results in a CSV log.

**Recorded observation:** Earlier samples included CPU-use values of approximately 16.30% and 13.60%. These are observations from individual samples, not a stable benchmark or performance guarantee.

**Why it matters:** Resource monitoring can help identify unexpectedly high CPU or memory use while scripts are running. It also introduces repeatable logging of measurements.

**Outcome:** Monitoring script and CSV logging were used in the Codespaces environment.

**Limitations:** Codespaces resource usage does not represent the performance of a different embedded computer. A target-device assessment requires measurements on the actual hardware under representative load.

### 5.3 Task-03 — Sensor Data Ingestion (7 October)

**Purpose:** Practice receiving or generating sensor-style records and organizing them for downstream processing.

**Work performed:** Developed a Python sensor-data ingestion demonstration and associated task notes or outputs as part of the task sequence.

**Why it matters:** Data-processing modules require a clear input structure. Ingestion is responsible for moving data into a form that later stages can validate, synchronize, analyze, or store.

**Outcome:** The task contributed to the sensor-processing workflow used in later demonstrations.

**Limitations:** A software ingestion demonstration does not prove compatibility with a physical sensor driver, serial port, I²C/SPI interface, packet format, or hardware timing requirements. Such interfaces need their own tests.

### 5.4 Task-04 — Embedded AI Inference (8 October)

**Purpose:** Run a small model-inference demonstration and record a prediction, confidence value, and execution time.

**Work performed:** Executed the inference script in the Python environment and saved the result to `Task-04/inference_results.csv`.

**Recorded example:** A previous run reported CPU execution, successful model loading, a Class 0 prediction, confidence of approximately `0.690895`, and inference time of approximately `18.1027 ms`.

**Why it matters:** This task demonstrates the basic inference lifecycle: prepare an input, pass it to a model, interpret the returned output, and record the result.

**Outcome:** A prediction and associated measurement were generated in the development environment.

**Limitations:** The available record does not establish that the model was trained and validated for a real drone application. A predicted class and confidence value are not, by themselves, evidence of classification accuracy or operational safety. The model, preprocessing, training data, and validation protocol must be documented before making such claims.

### 5.5 Task-05 — Inference Performance Benchmarking (9 October)

**Purpose:** Measure the execution latency of the inference demonstration under a defined software test.

**Work performed:** Ran 10 warm-up iterations followed by 100 measured CPU iterations, then recorded summary statistics.

**Previously recorded results:**

| Metric | Recorded value |
|---|---:|
| Warm-up runs | 10 |
| Measured runs | 100 |
| Average latency | 0.025377 ms |
| Median latency | 0.022693 ms |
| Minimum latency | 0.019887 ms |
| Maximum latency | 0.086772 ms |

The reciprocal of average latency was reported as an estimated throughput of approximately `39,405.51` operations per second. This is a mathematical estimate derived from the average latency, not an independently measured end-to-end throughput result.

**Why it matters:** Warm-up runs reduce the effect of initial execution overhead on the measured section. Repeated runs provide a distribution of timings rather than relying on a single measurement.

**Outcome:** The benchmark produced recorded latency statistics in the development environment.

**Limitations:** The measurement depends on the host, Python runtime, model, input size, and benchmark implementation. These figures do not establish latency on an embedded target, and they do not measure model accuracy.

### 5.6 Task-06 — Acoustic Sensing and TDoA Theory (10 October)

**Purpose:** Explore acoustic cross-correlation and the concept of Time Difference of Arrival.

**Work performed:** Generated synthetic acoustic signals, compared their timing through correlation, and recorded the estimated lag and associated plots/results.

**Recorded synthetic example:** A correlation lag of 48 samples at a sampling rate of 48,000 samples per second corresponds to:

```text
Time delay = lag / sampling rate
           = 48 / 48000
           = 0.001 seconds
           = 1 ms
```

Assuming a sound speed of `343 m/s`, the magnitude of the corresponding path difference is:

```text
Path-difference magnitude = sound speed × time delay
                          = 343 × 0.001
                          = 0.343 m
```

**Why it matters:** TDoA methods use differences in arrival time to infer relative path lengths. Correlation is one method for estimating the delay between two signals.

**Outcome:** The synthetic demonstration produced a lag estimate that could be converted into a path-difference magnitude under the stated assumptions.

**Limitations:** The example used synthetic periodic sine signals. Periodic signals may create multiple plausible correlation peaks. Real acoustic measurements also depend on noise, reflections, microphone characteristics, placement, sampling-clock alignment, and environmental conditions. The demonstration does not validate real acoustic localization.

### 5.7 Task-07 — Acoustic Signal Preprocessing (11 October)

**Purpose:** Practice preparing an acoustic signal before analysis.

**Recorded implementation details:**

- Signal: 1 kHz synthetic sine wave
- Sampling rate: 48 kHz
- Duration: 0.05 seconds
- Number of samples: 2,400
- Noise: reproducible Gaussian noise
- Smoothing: 5-sample moving-average filter
- Segmentation: five segments of 10 ms each
- Samples per segment: 480
- Outputs: CSV results and plots

**Why it matters:** Preprocessing can reduce some noise and organize a signal into smaller windows for later processing. Segmentation can help downstream algorithms operate on consistent intervals.

**Outcome:** The script generated the synthetic signal, applied the moving-average filter, segmented the data, and exported results.

**Limitations:** A moving-average filter smooths the signal and can also blur rapid changes. It is not guaranteed to be the best filter for every acoustic application. Synthetic signals do not reproduce all real microphone effects.

### 5.8 Task-08 — Sensor Synchronization (12 October)

**Purpose:** Align multiple timestamped sensor streams to a reference timeline.

**Recorded implementation details:**

- Streams: temperature, pressure, and humidity
- Samples: 20 per stream
- Nominal sampling interval: 100 ms
- Reference timeline: temperature timestamps
- Matching method: nearest timestamp
- Allowed difference: 40 ms
- Status labels: `SYNCED` and `OUT_OF_TOLERANCE`

**Recorded run:** 20 reference rows, 20 synchronized rows, and 0 out-of-tolerance rows.

**Why it matters:** Sensor readings captured at different times may not describe the same moment. Timestamp matching provides a simple way to combine nearby readings while explicitly checking a permitted timing difference.

**Outcome:** The synthetic run aligned the records under the configured tolerance and wrote the result to CSV.

**Limitations:** Nearest-timestamp matching does not correct sensor clock drift, does not interpolate values between samples, and may reuse a source reading. The result is not proof of synchronization accuracy with physical devices.

### 5.9 Task-09 — Fault and Dropout Handling (13 October)

**Purpose:** Identify invalid sensor values and missing readings, then test a fallback policy.

**Recorded test setup:** 12 synthetic samples, 8 valid readings, 2 faulty readings (including `-999` and `150` for a configured valid range of 0–100), and 2 dropouts represented as missing values.

**Work performed:** The demonstration checked readings against the configured valid range, identified missing readings, recorded status information, and used the last valid value as a fallback where the script's policy applied.

**Why it matters:** Sensor data can be invalid or absent. A processing pipeline should identify these cases rather than treating every value as trustworthy.

**Outcome:** Faults and dropouts were represented in the generated results, and a fallback approach was demonstrated.

**Limitations:** The range 0–100 is a demonstration-specific assumption, not a universal range for all sensors. A last-valid-value fallback can become stale if the sensor remains unavailable. Real deployments need sensor-specific limits, freshness checks, fault policies, and appropriate safe-state behavior.

### 5.10 Task-10 — Mini Module Assembly (14 October)

**Purpose:** Integrate sensor synchronization and fault/dropout handling into a combined demonstration pipeline.

**Main script:** `Task-10/mini_module.py`

**Associated files:**

- `Task-10/mini_module_results.csv`
- `Task-10/NOTES-T10.md`

**Recorded run:**

| Item | Recorded result |
|---|---:|
| Sensor streams | 3 |
| Samples per sensor | 20 |
| Reference rows | 20 |
| Synchronization tolerance | 40 ms |
| `SYNCED` rows | 20 |
| `OUT_OF_TOLERANCE` rows | 0 |
| Faulty readings | 2 |
| Dropout readings | 1 |

**Work performed:** Combined synthetic sensor generation, timestamp matching, validation, fault/dropout handling, fallback values, status tracking, and CSV reporting.

**Why it matters:** Individual processing steps can behave differently when integrated. The mini module checks whether these concepts can be connected into one repeatable software flow.

**Outcome:** The recorded synthetic run produced 20 reference rows and included fault/dropout handling in the generated output.

**Limitations:** No physical sensors were connected. Nearest-timestamp matching may reuse source samples and does not correct clock drift. A fallback value may become stale. The results do not demonstrate end-to-end performance on a real drone.

**Reproduction commands:**

```bash
python Task-10/mini_module.py
head -10 Task-10/mini_module_results.csv
```

### 5.11 Task-11 — Performance Optimization (15 October)

**Purpose:** Compare timestamp-search approaches and measure how runtime changes with dataset size.

**Main script:** `Task-11/performance_optimization.py`

**Methods compared:**

1. **Linear nearest-timestamp search:** Checks records sequentially to identify the closest timestamp.
2. **Binary-search-based lookup:** Uses sorted timestamp data and Python's `bisect` module to locate the insertion position, then considers neighboring candidates for nearest-timestamp selection.

The binary-search method requires sorted data. Correct nearest-value selection also requires handling the candidates around the insertion point and boundary cases such as a target before the first timestamp or after the last timestamp.

**Recorded dataset sizes:** 100, 500, 1,000, 2,000, and 4,000 records. The benchmark used repeated timing measurements and median summaries, and compared the outputs from the two methods.

**Previously saved benchmark results:**

| Dataset size | Linear median (ms) | Binary median (ms) | Speedup | Outputs match |
|---:|---:|---:|---:|:---:|
| 100 | 0.908006 | 0.027421 | 33.114× | Yes |
| 500 | 24.405157 | 0.183162 | 133.244× | Yes |
| 1,000 | 94.519656 | 0.368016 | 256.836× | Yes |
| 2,000 | 387.312080 | 0.793937 | 487.837× | Yes |
| 4,000 | 1,522.564064 | 2.545606 | 598.115× | Yes |

These values are from one saved run. Runtime measurements may differ on subsequent runs because of host load and execution conditions.

**Why it matters:** Optimization should be based on measurements and should preserve correctness. Comparing output values helps ensure that a faster approach is not simply returning different results.

**Outcome:** The saved run recorded matching outputs for all five dataset sizes, with the binary-search-based implementation faster in each tested case.

**Limitations:** The benchmark isolates timestamp lookup. It does not measure full sensor-pipeline latency, model inference, communication, or physical drone performance. Results should not be generalized to all hardware or workloads.

**Reproduction commands:**

```bash
python Task-11/performance_optimization.py
cat Task-11/performance_results.csv
```

### 5.12 Task-12 — Final Documentation and Package (16 October)

**Purpose:** Consolidate the technical report, testing summary, dependency information, and package checklist for review and handover.

**Expected artifacts:**

- `Task-12_Final-Documentation-Package/FINAL_REPORT.md`
- `Task-12_Final-Documentation-Package/TESTING_AND_RESULTS.md`
- `Task-12_Final-Documentation-Package/PACKAGE_CHECKLIST.md`
- `requirements.txt`

**Work focus:**

1. Summarize the tasks and the purpose of each demonstration.
2. Document recorded configurations and test outcomes.
3. Preserve assumptions and limitations, particularly the use of synthetic data.
4. Identify scripts and output files required to reproduce the demonstrations.
5. Document the development environment and Python dependencies.
6. Verify that paths and filenames in the report match the repository.
7. Review the package checklist and identify outstanding checks.
8. Inspect Git status and verify commit/push status before declaring handover complete.

**Outcome:** The final documentation package was prepared as a set of report, testing, checklist, and dependency artifacts.

**Status qualification:** The available record does not confirm that every file's final contents were fully reviewed, that every script was rerun as part of a final acceptance test, or that all Task-12 artifacts were committed and pushed. Therefore, final handover should be marked complete only after the checks in Section 10 are performed.

## 6. Overall Results and Evidence

### 6.1 Functional results

The task sequence produced software demonstrations and result artifacts for several processing stages. Recorded results include the Task-08 synchronization counts, Task-10 integration counts, and Task-11 benchmark table. These should be read as results from the recorded development-environment runs.

### 6.2 Timing results

Task-05 recorded inference timing for a small CPU demonstration. Task-11 recorded timing comparisons for timestamp-search algorithms across five dataset sizes. Both are software-environment measurements. They should be repeated on the intended target computer before using them to make deployment decisions.

### 6.3 What the results establish

The recorded demonstrations support the following limited conclusions:

- The scripts can exercise the described algorithmic workflows in the development environment.
- The synchronization and integration demonstrations can generate structured CSV results.
- The fault/dropout demonstration can identify configured invalid and missing values in its synthetic input.
- The saved Task-11 run showed matching outputs and lower measured lookup time for the binary-search-based approach on the tested datasets.

### 6.4 What the results do not establish

The recorded demonstrations do not establish:

- Accuracy with real microphones or physical sensors
- Real-world sensor-clock synchronization accuracy
- Robustness to every type of physical sensor fault or extended dropout
- Performance on a flight computer
- End-to-end latency of a complete drone system
- Operational classification accuracy of the inference model
- Safety or reliability of a deployed drone
- Validated flight-control behavior

## 7. Limitations and Risks

1. **Synthetic inputs:** Several demonstrations use generated rather than physical sensor data.
2. **No established drone deployment:** The work does not prove that the pipeline has been deployed to or validated on a real drone.
3. **Clock drift:** Timestamp matching does not automatically synchronize or correct sensor clocks.
4. **Sample reuse:** Nearest-timestamp matching may reuse a source reading unless one-to-one matching is explicitly enforced.
5. **Fallback freshness:** Last-valid-value handling may return stale data.
6. **Signal ambiguity:** Periodic acoustic signals can produce ambiguous correlation peaks.
7. **Benchmark variability:** Runtime depends on system load, runtime version, and measurement methodology.
8. **Sorted-data requirement:** Binary search requires sorted timestamps and careful boundary handling.
9. **Model validity:** A demonstration prediction does not establish training quality, accuracy, or suitability for a real application.
10. **Dependency portability:** A full environment freeze may include unrelated or platform-specific packages.
11. **Repository hygiene:** Local modifications and untracked directories need review before staging.
12. **Documentation completeness:** Documentation must match actual scripts and outputs.
13. **Safety boundary:** These demonstrations do not replace flight-control validation, hardware-in-the-loop testing, safety analysis, or field testing.

## 8. Future Scope and Recommendations

1. **Physical sensor integration:** Replace synthetic streams with recorded data from actual sensors when hardware is available.
2. **Timestamp quality:** Record clock source, timestamp units, sampling rate, and data-quality metadata explicitly.
3. **Clock-drift evaluation:** Test synchronization with offsets, drift, jitter, delayed packets, and out-of-order readings.
4. **Fallback safety:** Add maximum data-age checks and define behavior when no recent valid reading exists.
5. **Acoustic validation:** Use recorded microphone signals and evaluate correlation ambiguity, noise, and reflections.
6. **Target-hardware benchmarking:** Repeat inference and lookup benchmarks on the intended embedded computer.
7. **End-to-end measurement:** Measure the full pipeline, including input handling and output generation, rather than isolated functions only.
8. **Automated testing:** Add unit tests for valid readings, invalid readings, missing values, timestamp boundaries, empty inputs, and unsorted data.
9. **Dependency reproducibility:** Review and document the exact required packages and versions.
10. **Output verification:** Check every CSV against the script and the corresponding task notes.
11. **Version-control review:** Inspect staged changes, commit only intended files, and confirm the push result.
12. **Hardware validation plan:** Treat physical deployment as a separate engineering phase with appropriate verification and safety review.

## 9. Reproducibility and Execution Guide

### 9.1 Activate the environment

```bash
cd /workspaces/RE-T1
source .venv/bin/activate
which python
python --version
```

### 9.2 Inspect task files

```bash
ls Task-10
ls Task-11
ls Task-12_Final-Documentation-Package
```

If a folder or file is missing, use:

```bash
find . -maxdepth 2 -type f | sort
```

### 9.3 Run the integration demonstration

```bash
python Task-10/mini_module.py
head -10 Task-10/mini_module_results.csv
```

Review the printed summary and CSV together. The expected values in the recorded run are described in Section 5.10; a new run should be reported using its actual output.

### 9.4 Run the performance benchmark

```bash
python Task-11/performance_optimization.py
cat Task-11/performance_results.csv
```

Record the new timing values if this run is to be used as the report's benchmark. Do not combine timing values from different runs in one table without clearly identifying the source run.

### 9.5 Review documentation and dependencies

```bash
cat Task-12_Final-Documentation-Package/FINAL_REPORT.md
cat Task-12_Final-Documentation-Package/TESTING_AND_RESULTS.md
cat Task-12_Final-Documentation-Package/PACKAGE_CHECKLIST.md
cat requirements.txt
python -m pip list
```

The dependency list should be reviewed for relevance and portability. A package appearing in `requirements.txt` is not proof that it installed successfully in a different environment.

### 9.6 Verify repository status

```bash
git status --short --branch
git diff --check
```

Previously reported local state included modified Task-04 files and an untracked nested `RE-T1/` directory. Review those carefully. Do not accidentally stage unrelated files when preparing Task-12 documentation.

After reviewing the intended changes, inspect them before committing:

```bash
git diff -- Task-12_Final-Documentation-Package requirements.txt
git diff --cached
```

Commit only after confirming that the staged files are correct. Record the actual commit hash and confirm the push succeeded before describing the repository as up to date.

## 10. Final Handover Checklist

- [ ] Confirm every task script and referenced output file exists.
- [ ] Re-run applicable demonstrations and inspect the actual outputs.
- [ ] Ensure benchmark values match the exact CSV run being reported.
- [ ] Review the final report, testing/results summary, and package checklist.
- [ ] Review `requirements.txt` for relevant and portable dependencies.
- [ ] Keep synthetic-data and no-hardware-validation limitations explicit.
- [ ] Check `git status --short --branch`.
- [ ] Run `git diff --check`.
- [ ] Inspect the staged diff and exclude unrelated changes unless intentionally required.
- [ ] Commit only the intended files.
- [ ] Record the actual commit hash.
- [ ] Confirm the push succeeded.
- [ ] Obtain project lead review/sign-off where required.

## 11. Conclusion

The RE-T1 task sequence provided practical exposure to Linux resource monitoring, sensor-data processing, AI inference demonstration, acoustic signal analysis, timestamp synchronization, fault/dropout handling, algorithm benchmarking, and technical documentation.

Task-10 combined synchronization and fault/dropout handling into a synthetic demonstration pipeline. Task-11 compared linear and binary-search-based timestamp lookup and recorded faster lookup times for the binary-search-based approach in the saved benchmark run while checking output consistency. Task-12 consolidated the technical report, testing summary, dependency information, and package checks needed for review.

The central engineering lesson is that a result must be reported together with its configuration, evidence, and limitations. Synthetic demonstrations and software benchmarks are useful development evidence, but they are not equivalent to physical-sensor validation or proof of reliable operation on a drone. Final handover should be marked complete only after the documentation, scripts, dependencies, generated outputs, and Git repository state have been checked.

---

**Prepared by:** Ashish Thakur  
**Role:** Embedded AI Engineer  
**Date:** 16 October 2026
