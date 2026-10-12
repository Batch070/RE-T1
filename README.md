# RE-T1 — Embedded AI and Sensor Processing

## Overview

This repository contains task-wise implementations and documentation for sensor data processing, acoustic signal analysis, synchronization, fault handling, AI inference demonstrations, and performance optimization.

## Project Structure

- `Task-01/` — Architecture Orientation
- `Task-02/` — Linux Systems and Monitoring
- `Task-03/` — Sensor Data Ingestion
- `Task-04/` — Embedded AI Inference
- `Task-05/` — Inference Performance Benchmarking
- `Task-06/` — Acoustic Sensing and TDoA
- `Task-07/` — Acoustic Signal Preprocessing
- `Task-08/` — Sensor Synchronization
- `Task-09/` — Fault and Dropout Handling
- `Task-10/` — Mini Module Assembly
- `Task-11/` — Performance Optimization
- `Task-12_Final-Documentation-Package/` — Final Report, Testing Results, and Package Checklist

## Setup

Use Python 3 and create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Running a Demonstration

For example, run the performance optimization task:

```bash
python Task-11/performance_optimization.py
```

Other scripts can be run using their actual paths inside their respective task folders.

## Results

Tasks generate outputs such as CSV files, plots, and Markdown notes where applicable. Refer to each task's documentation for implementation details and results.

## Limitations

Several demonstrations use synthetic data. Benchmark results depend on the environment, and real hardware performance has not been established by synthetic-data experiments alone.

## Final Documentation

See `Task-12_Final-Documentation-Package/` for the final technical report, testing results, and package checklist.
