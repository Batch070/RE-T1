#!/usr/bin/env python3

import csv
import time
from pathlib import Path

import torch
import torch.nn as nn


BASE_DIR = Path(__file__).resolve().parent
RESULT_FILE = BASE_DIR / "inference_results.csv"


class SensorClassifier(nn.Module):
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
    print("=== RE-T1 Embedded AI Inference Demo ===")

    # Fixed seed for reproducible model initialization
    torch.manual_seed(42)

    # Use CPU for inference
    device = torch.device("cpu")
    print(f"Device: {device}")

    # Create and load the model
    model = SensorClassifier()
    model.to(device)
    model.eval()

    print("Model loaded successfully.")

    # Sensor input:
    # Temperature, Pressure, Humidity, Acceleration
    sensor_input = torch.tensor(
        [[28.5, 101.2, 63.4, 9.81]],
        dtype=torch.float32
    )

    sensor_input = sensor_input.to(device)

    print(f"Input tensor: {sensor_input.tolist()}")

    # Perform inference
    with torch.no_grad():

        start_time = time.perf_counter()

        output = model(sensor_input)

        end_time = time.perf_counter()

    # Calculate inference latency
    inference_time_ms = (end_time - start_time) * 1000

    # Convert model output into probabilities
    probabilities = torch.softmax(output, dim=1)

    # Select class with highest probability
    prediction = torch.argmax(probabilities, dim=1).item()

    # Get confidence of predicted class
    confidence = probabilities[0][prediction].item()

    # Display results
    print(f"Raw model output: {output.tolist()}")
    print(f"Prediction: Class {prediction}")
    print(f"Confidence: {confidence:.4f}")
    print(f"Inference time: {inference_time_ms:.4f} ms")

    # Save inference result to CSV
    with open(RESULT_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "temperature",
            "pressure",
            "humidity",
            "acceleration",
            "prediction",
            "confidence",
            "inference_time_ms"
        ])

        writer.writerow([
            28.5,
            101.2,
            63.4,
            9.81,
            prediction,
            round(confidence, 6),
            round(inference_time_ms, 6)
        ])

    print()
    print(f"Results saved to: {RESULT_FILE}")
    print("Inference completed successfully.")


if __name__ == "__main__":
    main()