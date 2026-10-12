
import bisect
import csv
import random
import statistics
import time
from pathlib import Path

# Task-11: Performance Optimization

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = OUTPUT_DIR / "performance_results.csv"

# Increasing dataset sizes for benchmarking.
DATASET_SIZES = [100, 500, 1000, 2000, 4000]
REPEATS = 3
SAMPLE_INTERVAL_MS = 100

random.seed(42)


def linear_nearest(timestamps, target):
    """Baseline: check every timestamp."""
    return min(
        range(len(timestamps)),
        key=lambda i: abs(timestamps[i] - target),
    )


def binary_nearest(timestamps, target):
    """Optimized: use binary search on sorted timestamps."""
    position = bisect.bisect_left(timestamps, target)

    if position == 0:
        return 0

    if position == len(timestamps):
        return len(timestamps) - 1

    previous_index = position - 1
    next_index = position

    previous_difference = abs(
        timestamps[previous_index] - target
    )
    next_difference = abs(
        timestamps[next_index] - target
    )

    # <= preserves the earlier sample when distances tie.
    if previous_difference <= next_difference:
        return previous_index

    return next_index


def benchmark(function, timestamps, targets):
    """Return median execution time in milliseconds."""
    measurements = []

    for _ in range(REPEATS):
        start = time.perf_counter()

        results = [
            function(timestamps, target)
            for target in targets
        ]

        elapsed_ms = (time.perf_counter() - start) * 1000
        measurements.append(elapsed_ms)

    return statistics.median(measurements), results


def main():
    results = []

    print("Task-11: Performance Optimization")
    print("---------------------------------")
    print(f"Repeats per method: {REPEATS}")
    print()

    for size in DATASET_SIZES:
        timestamps = [
            i * SAMPLE_INTERVAL_MS
            for i in range(size)
        ]

        # Use the same queries for both methods.
        targets = [
            random.randint(0, timestamps[-1])
            for _ in range(size)
        ]

        linear_ms, linear_results = benchmark(
            linear_nearest, timestamps, targets
        )

        binary_ms, binary_results = benchmark(
            binary_nearest, timestamps, targets
        )

        # Check correctness before reporting speedup.
        outputs_match = linear_results == binary_results

        if not outputs_match:
            raise RuntimeError(
                f"Output mismatch for dataset size {size}"
            )

        if binary_ms > 0:
            speedup = linear_ms / binary_ms
        else:
            speedup = 0.0

        improvement_percent = (
            (linear_ms - binary_ms) / linear_ms * 100
            if linear_ms > 0
            else 0.0
        )

        row = {
            "dataset_size": size,
            "queries": len(targets),
            "linear_median_ms": round(linear_ms, 6),
            "binary_median_ms": round(binary_ms, 6),
            "speedup": round(speedup, 3),
            "improvement_percent": round(
                improvement_percent, 2
            ),
            "outputs_match": outputs_match,
        }

        results.append(row)

        print(f"Dataset size: {size}")
        print(f"Linear search: {linear_ms:.6f} ms")
        print(f"Binary search: {binary_ms:.6f} ms")
        print(f"Speedup: {speedup:.3f}x")
        print(
            f"Time improvement: {improvement_percent:.2f}%"
        )
        print(f"Outputs match: {outputs_match}")
        print()

    with OUTPUT_FILE.open("w", newline="") as file:
        fieldnames = list(results[0].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
