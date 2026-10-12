# RE-T1 (SPECTRA) — Final Technical Report

## 1. Project Overview

RE-T1 is an embedded AI and sensor-processing development project focused on system monitoring, sensor data handling, acoustic signal processing, synchronization, fault handling, and performance optimization.

The project tasks were developed incrementally using Python, with synthetic datasets used for demonstrations and testing where physical hardware was unavailable.

## 2. Objectives

- Understand the system architecture and development environment.
- Monitor system resources and record measurements.
- Develop sensor data ingestion and AI inference demonstrations.
- Benchmark inference execution performance.
- Explore acoustic signal processing and Time Difference of Arrival (TDoA).
- Implement preprocessing and sensor timestamp synchronization.
- Detect invalid readings and missing sensor samples.
- Integrate the processing steps into a mini module.
- Compare alternative algorithms and document performance.
- Prepare a reproducible final project package.

## 3. Development Environment

- Operating environment: Linux-based GitHub Codespaces
- Programming language: Python
- Environment: Python virtual environment (`.venv`)
- Version control: Git and GitHub
- Data formats: CSV and Markdown
- Visualization: Matplotlib, where used
- Additional libraries: Refer to the actual imports and dependency files in the repository.

## 4. Work Completed

### Task 01 — Architecture Orientation
Reviewed the project architecture, components, and workflow.

### Task 02 — Linux Systems and Monitoring
Worked on system monitoring and recording system measurements.

### Task 03 — Sensor Data Ingestion
Developed the sensor data ingestion component.

### Task 04 — Embedded AI Inference
Developed an inference demonstration and recorded results. The model's training status and limitations must be stated accurately.

### Task 05 — Inference Performance Benchmarking
Benchmarked CPU inference execution. The recorded average latency was approximately 0.025377 ms for the measured run. This result applies to the tested implementation and environment.

### Task 06 — Acoustic Sensing and TDoA
Generated synthetic acoustic signals and used cross-correlation to estimate a time delay. The demonstrated delay was approximately 1 ms, corresponding to a path-difference magnitude of approximately 0.343 m under the assumed speed of sound of 343 m/s.

### Task 07 — Acoustic Signal Preprocessing
Generated a 1 kHz synthetic signal at 48 kHz, applied a moving-average filter, divided the signal into segments, and exported results.

### Task 08 — Sensor Synchronization
Implemented nearest-timestamp matching for synthetic temperature, pressure, and humidity streams using a 40 ms tolerance.

### Task 09 — Fault and Dropout Handling
Demonstrated detection of invalid sensor values and missing samples, with fallback values based on the last valid reading.

### Task 10 — Mini Module Assembly
Integrated synthetic sensor generation, timestamp synchronization, validation, fault/dropout handling, and CSV reporting.

### Task 11 — Performance Optimization
Compared linear nearest-timestamp search with binary-search-based lookup. Both methods returned matching outputs in the tested cases, and binary search was faster for all tested dataset sizes.

## 5. Overall Results

The project demonstrates individual sensor-processing and benchmarking techniques, including synchronization, fault detection, acoustic preprocessing, and algorithm comparison.

Most demonstrations use synthetic data. The recorded results should not be interpreted as validation on physical sensors or as proof of real-world drone performance.

## 6. Limitations

- Synthetic data is used in several demonstrations.
- Physical sensor and microphone validation has not been established by these experiments.
- Timestamp matching does not automatically correct sensor clock drift.
- Last-valid-value fallback can become stale.
- Benchmark results depend on the execution environment.
- AI inference results depend on the model and configuration used.
- Real-time performance and deployment on target hardware require separate validation.

## 7. Future Scope

- Integrate physical sensors and collect real measurements.
- Improve sensor clock synchronization and drift correction.
- Add configurable fault thresholds and recovery strategies.
- Evaluate the complete pipeline under realistic workloads.
- Validate inference on the intended embedded hardware.
- Add automated tests and dependency/version documentation.

## 8. Conclusion

The project establishes a modular foundation for sensor data processing, acoustic signal experimentation, synchronization, fault handling, and performance analysis. Further hardware-based testing and end-to-end validation are necessary before drawing conclusions about operational deployment.

## 9. Reproducibility

Refer to the root README for setup instructions, task locations, dependencies, and commands. Execute each demonstration using its actual script and verify the generated outputs before submission.