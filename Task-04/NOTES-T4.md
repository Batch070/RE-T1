# Task-04: Embedded AI Inference

## Project information

- **Project:** RudraEdge RE-T1 (Spectra)
- **Engineer:** Ashish Thakur
- **Role:** Embedded AI Engineer
- **Task order reference:** `REA/2026/RE-T1/TRAIN-001`
- **Assigned date:** 08 October 2026
- **Required output:** Basic inference demo
- **Execution environment:** GitHub Codespaces, Ubuntu Linux, Python virtual environment
- **Personal expenditure:** ₹0

## 1. Task objective

The goal was to demonstrate a basic AI inference workflow with a small neural network using local/open-source software. The model receives four sensor-like input features, executes a forward pass on CPU, converts its output to probabilities, selects a class index, measures elapsed inference time and saves the result to CSV.

**Scope note:** The network is not trained on labeled data. This is an inference-execution demonstration, not a validated sensor classifier.

## 2. What is inference?

Inference is the process of passing input data through an already-defined model to obtain its output. In a trained application, the model's learned parameters are used to produce a prediction. In this task, the network's architecture and forward pass are demonstrated, but the parameters are randomly initialized rather than trained for a real classification task.

A basic inference workflow is:

1. Prepare the input in the shape and data type expected by the model.
2. Place the model and input on the selected compute device.
3. Set evaluation mode.
4. Disable gradient tracking for inference.
5. Run the forward pass.
6. Interpret the output, for example with softmax and argmax.
7. Measure elapsed time and save the result.

## 3. Model architecture

The implemented network is:

```text
Input tensor: 4 features
        |
        v
Linear(4 -> 8)
        |
        v
      ReLU
        |
        v
Linear(8 -> 2)
        |
        v
  Two raw class scores
```

- **Input size 4:** temperature, pressure, humidity and acceleration.
- **First linear layer (4 → 8):** maps four input features to eight intermediate values.
- **ReLU:** applies a non-linear activation.
- **Second linear layer (8 → 2):** produces two raw output scores, one for each output class.

The model is implemented with `torch.nn.Module` and `torch.nn.Sequential`.

## 4. Input used in the recorded test

| Feature | Input |
|---|---:|
| Temperature | 28.5 |
| Pressure | 101.2 |
| Humidity | 63.4 |
| Acceleration | 9.81 |

The code does not specify a physical unit for the pressure value. The values are hard-coded test inputs, not live readings from a physical sensor or automatically imported from Task-03.

## 5. Key concepts and code behavior

### 5.1 Tensor

PyTorch tensors store numeric data. The input is represented as a two-dimensional tensor with shape `1 × 4`: one sample containing four features. The data type is `float32`.

### 5.2 CPU device

The script explicitly selects `torch.device("cpu")`. PyTorch was installed with a CUDA-enabled package build (`2.14.1+cu130` as reported by the environment), but `torch.cuda.is_available()` returned `False`; therefore, this test used CPU execution.

### 5.3 Evaluation mode

`model.eval()` places the model in evaluation mode. This matters for layers whose behavior differs between training and evaluation, such as dropout and batch normalization. The current simple network contains neither, but using evaluation mode is a good inference practice.

### 5.4 No gradient tracking

`torch.no_grad()` prevents autograd from tracking gradients during the forward pass. This reduces unnecessary inference overhead because this demo is not training the model.

### 5.5 Softmax

`torch.softmax(output, dim=1)` converts the two raw scores into normalized values that sum to 1 across the class dimension. These values are interpreted as class probabilities for this demonstration. Softmax does not make an untrained model accurate or calibrated.

### 5.6 Argmax and confidence

`torch.argmax(probabilities, dim=1)` selects the index with the largest probability. The confidence value is the softmax probability at that selected index.

Because the model is untrained, the selected class and confidence must not be interpreted as a verified real-world condition or diagnosis.

### 5.7 Inference latency

The script uses `time.perf_counter()` immediately before and after the model forward pass and converts the elapsed time to milliseconds. This is a single observed measurement; it is not a robust benchmark. Later benchmarking should include warm-up runs, many repetitions and summary statistics.

### 5.8 Reproducibility

`torch.manual_seed(42)` is set before constructing the model so its random initialization can be repeated under the same relevant software/runtime conditions. The measured latency may still vary from run to run.

## 6. Recorded result

The first successful run recorded the following:

| Metric | Result |
|---|---:|
| Device | CPU |
| Prediction | Class 0 |
| Confidence | `0.690895` (about 69.09%) |
| Inference time | `18.102666 ms` |
| CSV output | `Task-04/inference_results.csv` |

These are the values from the recorded run. Latency can vary between runs and should be measured repeatedly for performance analysis.

## 7. CSV format

The output CSV contains one header row and one result row:

```csv
temperature,pressure,humidity,acceleration,prediction,confidence,inference_time_ms
28.5,101.2,63.4,9.81,0,0.690895,18.102666
```

The script writes the result file in write mode, so the latest run replaces the previous CSV contents.

## 8. Tools and environment

- Python 3.14.2
- PyTorch reported as `2.14.1+cu130`
- NumPy 2.5.3
- Python standard-library `csv`, `time`, `pathlib`
- Bash/Linux CLI
- Git and GitHub Codespaces
- Project-local `.venv` virtual environment

The initial PyTorch check reported that NumPy was missing. NumPy was installed and subsequently verified. A Python seed statement was also accidentally entered in Bash; it was moved into the Python file where it belongs.

## 9. Repository outputs

```text
Task-04/
├── inference_demo.py
├── inference_results.csv
└── NOTES.md
```

The root `.gitignore` should ignore `.venv/`, `__pycache__/` and `*.pyc`.

Repository: `https://github.com/Batch070/RE-T1`  
Reported push commit: `bc8327f`

## 10. Testing and run instructions

From the repository root, with the virtual environment active:

```bash
python -m py_compile Task-04/inference_demo.py
python Task-04/inference_demo.py
cat Task-04/inference_results.csv
```

A successful `py_compile` command normally prints nothing. The script should print the selected device, input tensor, raw model output, predicted class, confidence, inference time and CSV path.

## 11. Limitations and recommended improvements

- The model is untrained; output class and confidence are only demonstration outputs.
- Input values are hard-coded rather than loaded from the Task-03 validated CSV.
- There is only one test input in the current demo.
- A single latency measurement is sensitive to warm-up and environment noise.
- There is no accuracy evaluation because there is no labeled test dataset.
- The pressure input's physical unit is not declared in the code.

Potential future improvements, if included in a later task, are to benchmark repeated inference, track process memory and CPU use, and clearly document the warm-up and measurement method.

## 12. Outcome

A basic PyTorch inference script ran successfully on CPU, generated a class output and softmax confidence, measured elapsed forward-pass time and saved the result to CSV. The code passed a Python syntax check and the work was pushed to the GitHub repository.

## 13. Next assigned task

**Task-05 — Inference Performance Benchmarking:** measure repeated inference latency, CPU utilization and memory consumption, then document the measurement methodology and limitations.
