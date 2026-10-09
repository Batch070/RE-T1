
import csv
import time
import statistics
from pathlib import Path

import torch
import torch.nn as nn


class InferenceModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 2)
        )

    def forward(self, x):
        return self.network(x)


def main():
    torch.manual_seed(42)
    torch.set_num_threads(1)

    model = InferenceModel()
    model.eval()

    input_data = torch.tensor(
        [[28.5, 101.2, 63.4, 9.81]],
        dtype=torch.float32
    )

    warmup_runs = 10
    benchmark_runs = 100
    latencies = []
    results = []

    with torch.inference_mode():
        # Warm-up: these runs are not measured
        for _ in range(warmup_runs):
            model(input_data)

        # Measure 100 inference runs
        for run in range(1, benchmark_runs + 1):
            start = time.perf_counter_ns()
            output = model(input_data)
            end = time.perf_counter_ns()

            latency_ms = (end - start) / 1_000_000
            probabilities = torch.softmax(output, dim=1)[0]
            predicted_class = int(torch.argmax(probabilities).item())
            confidence = float(probabilities[predicted_class].item())

            latencies.append(latency_ms)
            results.append({
                "run": run,
                "latency_ms": round(latency_ms, 6),
                "predicted_class": predicted_class,
                "confidence": round(confidence, 6)
            })

    avg_ms = statistics.mean(latencies)
    median_ms = statistics.median(latencies)
    min_ms = min(latencies)
    max_ms = max(latencies)
    throughput = 1000 / avg_ms if avg_ms > 0 else 0

    output_file = Path("Task-05/benchmark_results.csv")
    with output_file.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "run", "latency_ms",
                "predicted_class", "confidence"
            ]
        )
        writer.writeheader()
        writer.writerows(results)

    print("\n=== Task-05 Performance Benchmark ===")
    print(f"Device: CPU")
    print(f"Warm-up runs: {warmup_runs}")
    print(f"Measured runs: {benchmark_runs}")
    print(f"Average latency: {avg_ms:.6f} ms")
    print(f"Median latency:  {median_ms:.6f} ms")
    print(f"Minimum latency: {min_ms:.6f} ms")
    print(f"Maximum latency: {max_ms:.6f} ms")
    print(f"Approx. throughput: {throughput:.2f} inferences/sec")
    print(f"CSV saved to: {output_file}")


if __name__ == "__main__":
    main()
