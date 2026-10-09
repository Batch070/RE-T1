# Task-05: Inference Performance Benchmarking

**Project:** RE-T1 — Embedded AI Training  
**Task date:** 9 October 2026  
**Task folder:** `Task-05/`  
**Benchmark script:** `benchmark_inference.py`  
**Results file:** `benchmark_results.csv`

---

## 1. Objective

The objective of Task-05 was to measure the execution performance of a small PyTorch neural network by running repeated inference operations and recording their latency.

Task-04 focused on implementing and running a basic inference pipeline. Task-05 focuses on measuring that pipeline's performance. The goal is to learn how to collect repeatable timing measurements, summarize them with basic statistics, and save the results for later inspection.

## 2. Background: What Is Inference?

Inference is the process of passing input data through an existing model to obtain an output. In this practical, the model accepts four numerical features and produces two output scores.

The model used in this benchmark is a small feedforward neural network implemented in PyTorch. It has two fully connected (`Linear`) layers and one ReLU activation:

- Input features: 4
- First linear layer: 4 → 8
- Activation: ReLU
- Output layer: 8 → 2

The model is **untrained**. Therefore, its output is only a demonstration of the inference process. The predicted class and confidence must not be interpreted as validated real-world predictions or accuracy.

## 3. Environment and Tools

- Platform: GitHub Codespaces
- Operating system: Ubuntu environment in Codespaces
- Language: Python
- ML framework: PyTorch
- Execution device: CPU
- Timing function: `time.perf_counter_ns()`
- Result format: CSV

The benchmark was run inside the active Python virtual environment shown by the terminal prompt (`.venv`). The recorded environment did not have CUDA GPU execution available for this run, so the benchmark used CPU inference.

## 4. Input Data

The script uses one fixed input tensor with four numerical values:

| Feature | Value | Role in the demo |
|---|---:|---|
| Temperature | 28.5 | First numerical input |
| Pressure | 101.2 | Second numerical input |
| Humidity | 63.4 | Third numerical input |
| Acceleration | 9.81 | Fourth numerical input |

These are demo values, not readings collected from connected physical sensors.

## 5. Model Architecture

The benchmark defines this network:

```python
nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 2)
)
```

### Layer-by-layer explanation

1. **`nn.Linear(4, 8)`** — accepts four input features and calculates eight output values using learned parameters (weights and biases).
2. **`nn.ReLU()`** — applies the function `f(x) = max(0, x)`, replacing negative values with zero and leaving positive values unchanged.
3. **`nn.Linear(8, 2)`** — maps the eight intermediate values to two output scores.

The model is initialized with `torch.manual_seed(42)` to make its initial random parameters reproducible in the same setup. This does not train the network.

## 6. Benchmark Procedure

### 6.1 Model setup

The script creates the model, selects evaluation mode using `model.eval()`, and prepares the input tensor.

### 6.2 Warm-up runs

The script performs 10 warm-up runs before collecting measurements. These runs are not included in the reported benchmark results. Warm-up helps separate initial execution effects from the measured runs, although it does not eliminate all system noise.

### 6.3 Measured runs

The script measures 100 forward passes. Before each pass it records a start timestamp with `time.perf_counter_ns()` and records an end timestamp after the forward pass. The difference is converted from nanoseconds to milliseconds:

```python
latency_ms = (end - start) / 1_000_000
```

The timing interval measures the model's forward pass. It does not include model initialization, input creation, CSV writing, or the subsequent softmax/class-selection operations.

### 6.4 Inference mode

The benchmark uses `torch.inference_mode()` to avoid autograd-related overhead that is unnecessary for inference. It also uses `model.eval()` to place the model in evaluation mode.

### 6.5 Recorded fields

For each measured run, the CSV records:

- `run` — sequential run number from 1 to 100
- `latency_ms` — measured forward-pass latency in milliseconds
- `predicted_class` — class selected from the output scores
- `confidence` — the selected class's softmax score

Because the model is untrained, the class and confidence are for demonstration only.

## 7. Results

The benchmark script completed successfully and printed the following measurements:

| Metric | Recorded result |
|---|---:|
| Device | CPU |
| Warm-up runs | 10 |
| Measured runs | 100 |
| Average latency | 0.025377 ms |
| Median latency | 0.022693 ms |
| Minimum latency | 0.019887 ms |
| Maximum latency | 0.086772 ms |
| Approximate throughput estimate | 39,405.51 inferences/second |

### 7.1 Interpreting the measurements

- **Average latency (0.025377 ms):** the arithmetic mean of the 100 measured forward-pass durations.
- **Median latency (0.022693 ms):** the middle value after sorting the measured durations.
- **Minimum latency (0.019887 ms):** the shortest measured duration.
- **Maximum latency (0.086772 ms):** the longest measured duration.
- **Approximate throughput estimate (39,405.51 inferences/second):** calculated as `1000 / average_latency_ms`. It is an estimate derived from latency, not a separately measured sustained throughput result.

The maximum latency is higher than the median, indicating that at least one run took noticeably longer than the typical run. Small timing measurements can vary because of operating-system scheduling, virtualized CPU conditions, timer overhead, and other processes.

## 8. Why Performance Benchmarking Matters

A model can generate a prediction but still be unsuitable for a time-sensitive embedded application if its execution is too slow or inconsistent.

Benchmarking helps engineers:

1. Measure how long the model's forward pass takes.
2. Observe timing variation across repeated runs.
3. Compare model versions or runtime configurations under consistent conditions.
4. Check whether a model might meet a system's latency requirements.
5. Establish a baseline before testing on actual target hardware.

This benchmark was performed in Codespaces, not on a physical embedded board. Therefore, the results describe this specific cloud CPU environment and should not be treated as the performance of a drone, microcontroller, Raspberry Pi, or other target device.

## 9. Limitations

1. **Untrained model:** The model has not learned from a labelled dataset, so prediction quality and real-world accuracy are unknown.
2. **Cloud CPU environment:** Results may differ on a local computer or embedded device.
3. **Small model and fixed input:** The benchmark covers one tiny network and one input shape.
4. **Short measurements:** Sub-millisecond timing is sensitive to scheduling and measurement overhead.
5. **Estimated throughput:** Throughput was calculated from average latency rather than measured using a sustained concurrent or batch workload.
6. **Limited metrics:** This script does not measure peak memory use, energy consumption, model accuracy, or end-to-end sensor-to-decision latency.

## 10. Reproduction Instructions

Run these commands from the repository root in Codespaces:

```bash
python Task-05/benchmark_inference.py
```

Inspect the CSV output:

```bash
head Task-05/benchmark_results.csv
```

Count the lines:

```bash
wc -l Task-05/benchmark_results.csv
```

If the benchmark ran successfully with 100 measured runs, the CSV should normally contain 101 lines: one header row and 100 data rows.

## 11. Output Files

- `Task-05/benchmark_inference.py` — benchmark implementation.
- `Task-05/benchmark_results.csv` — per-run latency, predicted class, and confidence.

## 12. Conclusion

Task-05 successfully demonstrated a basic inference performance benchmarking workflow. The script ran 10 warm-up iterations, measured 100 CPU forward passes, calculated latency statistics, estimated throughput from average latency, and saved per-run measurements to CSV.

The work builds on Task-04: Task-04 demonstrated how a model produces an output, while Task-05 measured the execution time and variability of the model's forward pass. The results are a baseline for learning and comparison, not evidence of real-world model accuracy or target-hardware performance.

## 13. Suggested Next Improvements

- Repeat the benchmark several times and compare run-to-run statistics.
- Report percentiles such as p90 and p95 latency.
- Measure sustained throughput separately with a defined workload.
- Measure memory usage and power consumption where supported.
- Benchmark a trained and validated model.
- Compare performance on the intended embedded target hardware.
