# Testing and Results

## 1. Testing Approach

Each task should be checked independently before final packaging.

- Confirm that the relevant script exists.
- Run the script in the project's Python virtual environment.
- Check its exit status and terminal output.
- Verify that expected CSV files, plots, or reports are generated.
- Inspect CSV headers and sample rows.
- Record any errors or limitations.

## 2. Recorded Benchmark Results

### Inference Benchmark

The previously recorded CPU benchmark reported:

- Average latency: approximately 0.025377 ms
- Median latency: approximately 0.022693 ms
- Minimum latency: approximately 0.019887 ms
- Maximum latency: approximately 0.086772 ms

These values describe the specific recorded benchmark, not a guaranteed deployment performance.

### Timestamp Search Optimization

| Dataset size | Linear median (ms) | Binary median (ms) | Speedup |
|---:|---:|---:|---:|
| 100 | 0.908006 | 0.027421 | 33.114× |
| 500 | 24.405157 | 0.183162 | 133.244× |
| 1,000 | 94.519656 | 0.368016 | 256.836× |
| 2,000 | 387.312080 | 0.793937 | 487.837× |
| 4,000 | 1522.564064 | 2.545606 | 598.115× |

All five recorded comparisons reported matching outputs.

## 3. Sensor Synchronization

The recorded Task-08 demonstration used three synthetic sensor streams, 20 samples per sensor, and a 40 ms timestamp tolerance. The recorded run produced 20 synchronized rows and zero out-of-tolerance rows.

## 4. Fault and Dropout Handling

The recorded Task-09 demonstration processed 12 samples:

- Valid samples: 8
- Faulty samples: 2
- Dropout samples: 2

Task-10 also demonstrated integrated synchronization and sensor validation. Its results must be checked against the generated CSV before submission.

## 5. Validation Limitations

The reported values are from specific demonstrations and benchmark runs. Results can vary across machines and runs. Synthetic-data tests do not establish performance with physical sensors, environmental noise, or real-time deployment conditions.

## 6. Final Verification Record

Before submission, record:

- Date of final verification
- Python version
- Installed dependencies
- Scripts executed successfully
- Output files checked
- Known issues
- Final Git commit hash
