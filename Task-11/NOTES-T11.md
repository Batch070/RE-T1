# Task-11: Performance Optimization

## 1. Objective

The objective of this task is to evaluate and demonstrate a performance optimization technique for timestamp matching in sensor-processing systems.

The task compares a baseline linear-search algorithm with an optimized binary-search algorithm. Both algorithms identify the nearest timestamp to a target time. Their execution times are measured on multiple dataset sizes, and their outputs are compared to verify correctness.

The main objectives are:

- To understand the importance of performance optimization in embedded systems.
- To establish a baseline execution-time measurement.
- To implement an optimized nearest-timestamp search.
- To compare execution times across different dataset sizes.
- To verify that the optimized method produces the same results as the baseline method.
- To calculate speedup and percentage time improvement.
- To export benchmark results to a CSV file.

## 2. Introduction

Performance optimization is the process of improving a program's execution efficiency while preserving its required behavior.

Embedded systems often operate with limited processing power, memory, and energy. Efficient algorithms can reduce processing time and help a system handle increasing amounts of sensor data.

The Task-10 mini module performs timestamp matching as part of its sensor synchronization workflow. The baseline nearest-timestamp function searches the entire sensor stream to find the closest timestamp.

For larger datasets, repeatedly scanning every timestamp can require significant processing time.

This task evaluates an alternative approach based on binary search. Because binary search works on sorted data, it can identify the insertion position of a target timestamp without checking every element.

The benchmark compares the two approaches using synthetic timestamp datasets.

## 3. Performance Optimization Concepts

### 3.1 Execution Time

Execution time is the amount of time a program or operation takes to complete.

In this task, execution time is measured using Python's `time.perf_counter()` function.

The timer measures the duration of the timestamp-matching operation. The results are expressed in milliseconds.

### 3.2 Baseline

A baseline is the reference implementation against which an optimization is compared.

In this task, linear search acts as the baseline.

The optimized implementation is compared against it using the same timestamp data and target queries.

### 3.3 Time Complexity

Time complexity describes how the amount of computational work grows as the input size increases.

For one nearest-timestamp query:

- Linear search has worst-case time complexity of O(n).
- Binary search has time complexity of O(log n).

Here, n represents the number of timestamps in a sensor stream.

If n queries are performed on a stream of n timestamps, repeated linear searches may require O(n²) total search work, while binary searches require O(n log n) total search work, assuming the timestamp stream is already sorted.

These are algorithmic complexity estimates, not direct measurements of execution time.

### 3.4 Speedup

Speedup expresses how much faster the baseline is compared with the optimized implementation.

Speedup = Baseline Execution Time / Optimized Execution Time

For example, if the baseline takes 10 ms and the optimized implementation takes 2 ms:

Speedup = 10 / 2 = 5

This represents a fivefold speedup for the measured operation.

### 3.5 Percentage Time Improvement

Percentage time improvement expresses the reduction in execution time relative to the baseline.

Percentage Improvement = ((Baseline Time − Optimized Time) / Baseline Time) × 100

For example, reducing execution time from 10 ms to 2 ms gives:

Percentage Improvement = ((10 − 2) / 10) × 100 = 80%

The actual improvement in this experiment must be calculated from the measured results.

## 4. System Configuration

The benchmark uses the following configuration:

| Parameter | Value |
|---|---|
| Programming language | Python 3 |
| Dataset sizes | 100, 500, 1000, 2000, 4000 |
| Timestamp interval | 100 ms |
| Queries per dataset | Equal to the dataset size |
| Repetitions per method | 3 |
| Timing method | `time.perf_counter()` |
| Reported timing | Median of repeated measurements |
| Output format | CSV |
| Output file | `Task-11/performance_results.csv` |

A fixed random seed is used to generate reproducible target queries.

## 5. Baseline Algorithm: Linear Search

### 5.1 Working Principle

Linear search checks every timestamp and identifies the index with the smallest absolute difference from the target timestamp.

For a target timestamp t and a candidate timestamp s, the difference is:

Difference = |s − t|

The candidate with the smallest difference is selected.

If two candidates have equal differences, the implementation selects the earlier candidate in the list.

### 5.2 Advantages

- Simple to understand and implement.
- Works with an unsorted list of timestamps.
- Provides a straightforward reference implementation.
- Useful for small datasets.

### 5.3 Limitations

- Every query may require checking the entire list.
- Repeated searches become expensive as the dataset grows.
- The computational work can increase significantly when many reference timestamps must be matched.

## 6. Optimized Algorithm: Binary Search

### 6.1 Working Principle

Binary search operates on a sorted timestamp list.

Python's `bisect.bisect_left()` identifies the position where a target timestamp could be inserted while preserving sorted order.

The algorithm then checks the nearest candidate on either side of that position.

It compares the absolute differences and selects the closer timestamp.

If the two differences are equal, the implementation chooses the earlier candidate to preserve the baseline's tie-breaking behavior.

### 6.2 Advantages

- Requires logarithmic search time for each query.
- Reduces repeated timestamp comparisons for larger datasets.
- Is suitable for timestamp matching when the input stream is sorted.
- Can reduce the computational cost of sensor synchronization.

### 6.3 Limitations

- The timestamp list must be sorted.
- Sorting an unsorted list introduces an additional cost.
- For very small datasets, the improvement may be small or the optimized method may be slower due to function-call and setup overhead.
- Performance depends on dataset size, input distribution, and the execution environment.

## 7. Benchmark Methodology

The experiment follows a controlled comparison procedure.

### Step 1: Generate Timestamp Data

The program creates sorted timestamps separated by a nominal interval of 100 milliseconds.

### Step 2: Generate Target Queries

The program generates target timestamps using a fixed random seed.

Both algorithms receive the same targets for each dataset size.

### Step 3: Measure Linear Search

The baseline algorithm processes all target queries. The total elapsed time is measured.

### Step 4: Measure Binary Search

The optimized algorithm processes the same queries. Its total elapsed time is measured independently.

### Step 5: Repeat Measurements

Each method is measured three times. The median measurement is used to reduce the influence of unusually fast or slow runs.

### Step 6: Verify Correctness

The selected timestamp indices from both algorithms are compared.

If the results differ, the benchmark raises an error rather than reporting the comparison as successful.

### Step 7: Calculate Performance Metrics

The program calculates speedup and percentage time improvement using the measured median execution times.

### Step 8: Save the Results

All measurements and correctness checks are written to a CSV file.

## 8. Implementation Details

### 8.1 `linear_nearest()`

This function implements the baseline algorithm.

It examines the full timestamp list and returns the index of the timestamp nearest to the target.

### 8.2 `binary_nearest()`

This function implements the optimized algorithm.

It uses binary search to find the insertion position and compares neighboring timestamps to identify the closest candidate.

### 8.3 `benchmark()`

This function measures the elapsed time for repeated executions of a search method.

It returns the median execution time and the search results.

### 8.4 Correctness Verification

The benchmark compares the output indices from the linear and binary implementations.

The `outputs_match` field is set to `True` when the outputs are identical.

This check helps ensure that the observed performance comparison is not achieved by changing the required nearest-timestamp result.

### 8.5 Performance Calculations

The program calculates:

- Baseline median execution time.
- Optimized median execution time.
- Speedup ratio.
- Percentage time improvement.
- Output equivalence.

### 8.6 CSV Reporting

The results are saved to:

`Task-11/performance_results.csv`

The CSV supports inspection and comparison across all configured dataset sizes.

## 9. Execution Procedure

Activate the project's virtual environment and run the benchmark from the repository root:

`python Task-11/performance_optimization.py`

The program prints the dataset size, linear-search time, binary-search time, speedup, percentage improvement, and correctness result.

Inspect the generated report using:

`head -n 10 Task-11/performance_results.csv`

The file contains the measurements for all configured dataset sizes.

## 10. Output File Structure

The benchmark CSV contains the following columns:

| Column | Description |
|---|---|
| `dataset_size` | Number of timestamps in the dataset. |
| `queries` | Number of target queries processed. |
| `linear_median_ms` | Median execution time of linear search in milliseconds. |
| `binary_median_ms` | Median execution time of binary search in milliseconds. |
| `speedup` | Ratio of baseline time to optimized time. |
| `improvement_percent` | Percentage reduction in execution time. |
| `outputs_match` | Whether both implementations return identical indices. |

The report allows performance and correctness to be evaluated together.

## 11. Experimental Results

The benchmark evaluates five dataset sizes: 100, 500, 1000, 2000, and 4000 timestamps.

Each dataset is tested with the same number of target queries as timestamps. Both methods are repeated three times, and their median execution times are recorded.

Fill in the table using the values from the generated CSV file.

| Dataset Size | Linear Median (ms) | Binary Median (ms) | Speedup | Outputs Match |
|---:|---:|---:|---:|---|
| 100 | Enter measured value | Enter measured value | Enter measured value | Enter measured result |
| 500 | Enter measured value | Enter measured value | Enter measured value | Enter measured result |
| 1000 | Enter measured value | Enter measured value | Enter measured value | Enter measured result |
| 2000 | Enter measured value | Enter measured value | Enter measured value | Enter measured result |
| 4000 | Enter measured value | Enter measured value | Enter measured value | Enter measured result |

### 11.1 Interpretation

The benchmark is designed to show how execution time changes as the timestamp dataset grows.

Linear search performs a full scan for every query, while binary search reduces the search range at each step.

For larger datasets, binary search is expected to reduce the search work. However, the actual speedup must be determined from the measured results.

For small datasets, binary search may show a limited improvement or even take longer because of implementation overhead.

The `outputs_match` column must remain `True` for every dataset before the performance comparison is accepted as correct.

## 12. Tools and Technologies

The task uses:

- Python 3.
- Python standard-library modules.
- `time.perf_counter()` for timing.
- `statistics.median()` for repeated measurements.
- `bisect` for binary search.
- CSV for storing benchmark results.
- GitHub Codespaces for development.
- Git and GitHub for version control.

No third-party Python package is required.

## 13. Limitations

### 13.1 Synthetic Workload

The benchmark uses generated timestamp data rather than live sensor streams.

### 13.2 Isolated Algorithm Benchmark

The experiment measures timestamp-matching functions. It does not measure the complete Task-10 module, sensor acquisition, or AI inference latency.

### 13.3 Machine-Dependent Results

Execution times depend on CPU performance, system load, interpreter overhead, and other environmental factors.

### 13.4 Small Benchmark Sizes

The largest tested dataset contains 4000 timestamps. Larger datasets could provide additional information about scaling behavior.

### 13.5 Sorting Assumption

Binary search requires sorted timestamps. If real sensor timestamps are unsorted, preprocessing or another data structure may be necessary.

### 13.6 No Memory Benchmark

The implementation measures execution time but does not directly measure memory usage or energy consumption.

### 13.7 No Hardware-Level Optimization

The task does not modify firmware, CPU frequency, hardware configuration, or AI model architecture.

## 14. Future Improvements

The benchmark can be extended by:

- Testing larger datasets.
- Benchmarking the complete Task-10 workflow.
- Measuring memory usage.
- Recording CPU utilization.
- Evaluating different timestamp distributions.
- Testing irregular sampling intervals.
- Measuring performance under realistic sensor workloads.
- Adding automated correctness tests.
- Evaluating the impact of preprocessing and sorting costs.
- Integrating profiling into the embedded AI pipeline.

## 15. Conclusion

Task-11 demonstrates a performance optimization approach for timestamp matching.

A linear-search implementation is used as the baseline, while a binary-search implementation is evaluated as the optimized alternative. Both methods process identical timestamp datasets and target queries.

Execution time, speedup, percentage time improvement, and output equivalence are measured and saved to a CSV report.

The task demonstrates that algorithm selection can influence performance as sensor datasets grow. The actual improvement must be established using the measured benchmark results, while output equivalence verifies that the optimization preserves the required matching behavior.

The experiment provides a foundation for further performance analysis of integrated sensor-processing and embedded AI systems.