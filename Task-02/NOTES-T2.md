# Task-02: Linux Systems & Monitoring

## Project information

- **Project:** RudraEdge RE-T1 (Spectra)
- **Engineer:** Ashish Thakur
- **Role:** Embedded AI Engineer
- **Task order reference:** `REA/2026/RE-T1/TRAIN-001`
- **Assigned date:** 06 October 2026
- **Required output:** System monitoring script
- **Execution environment:** GitHub Codespaces, Ubuntu 24.04.5 LTS
- **Personal expenditure:** ₹0

## 1. Task objective

The objective was to understand basic Linux system monitoring and implement a Python script that collects system resource metrics and saves them in a CSV file. This establishes a baseline for observing the compute environment before running more demanding sensor-processing and AI-inference workloads.

**Environment clarification:** The implementation was run in GitHub Codespaces, a cloud-hosted Ubuntu environment. Its metrics describe that Codespaces machine and should not be represented as measurements from a physical laptop.

## 2. Why system monitoring matters for Embedded AI

Embedded AI applications operate with limited compute, memory, power and thermal budgets. Before optimizing an inference pipeline, engineers need to know how much CPU and memory it uses and whether resource consumption changes during repeated execution.

System monitoring can help answer questions such as:

- Is the CPU busy or mostly idle?
- How much RAM is available?
- Which processes are consuming resources?
- Does the application cause memory use to increase over time?
- Is the machine under sustained load?
- How long has the system been running?

For this training task, the monitoring script provides a basic system-level measurement tool. It is not itself an embedded-device power or temperature monitor.

## 3. Concepts studied

### 3.1 CPU utilization

CPU utilization estimates how much processor time is being used during a sampling interval. It is commonly expressed as a percentage.

- A high value can indicate compute-intensive activity.
- A low value indicates that the CPU was less busy during that sample.
- A single sample is not enough to establish a stable performance baseline.

`psutil.cpu_percent(interval=1)` waits for a one-second sampling interval and reports CPU utilization over that interval.

### 3.2 Logical CPU count

Logical CPU count is the number of logical processors visible to the running environment. The recorded Codespaces environment exposed **2 logical CPUs**. This is a property of the environment available to the process, not necessarily the physical host's complete CPU configuration.

### 3.3 RAM and memory utilization

The script uses virtual-memory information to record fields such as:

- Total memory
- Used memory
- Available memory
- Memory utilization percentage

Memory utilization can change as processes start, stop or allocate memory. When comparing runs, use the same environment and workload where possible.

### 3.4 Swap

Swap is disk-backed space that an operating system may use to support memory management. The recorded check showed **0 MB swap usage**. That is an observation from the tested environment, not a guarantee that every run or machine will report zero.

### 3.5 Processes

A process is a running program instance. Process monitoring can include:

- Process ID (PID)
- Process name
- CPU utilization
- Memory consumption

Commands such as `ps` and `top` provide independent ways to inspect processes and cross-check the script's output.

### 3.6 Uptime and load average

- **Uptime** is the time elapsed since system boot.
- **Load average** summarizes runnable or uninterruptible work over 1-, 5- and 15-minute periods on Linux systems where the values are available.

Load average is not the same as CPU utilization. Interpret it together with the number of logical CPUs and the workload.

### 3.7 CSV logging

CSV (Comma-Separated Values) stores tabular data as rows and columns. Recording a timestamp with each sample allows measurements from different points in time to be compared or plotted later.

## 4. Implementation details

A Python system-monitoring script was created using `psutil`. Its monitoring scope includes:

1. Timestamping each sample.
2. Measuring CPU utilization.
3. Recording logical CPU count.
4. Collecting RAM and swap statistics.
5. Calculating uptime from system boot time.
6. Collecting Linux load averages where supported.
7. Inspecting processes and identifying high-CPU processes.
8. Writing collected measurements to a CSV output file.
9. Supporting configurable sampling interval, number of samples and output path.

The script is intended to collect a series of observations rather than a single snapshot.

## 5. Tools and environment

Recorded environment information:

| Item | Recorded value |
|---|---|
| Operating system | Ubuntu 24.04.5 LTS |
| Python | 3.14.2 |
| Git | 2.55.0 |
| GCC | 13.3.0 |
| `psutil` | 7.2.2 |
| Logical CPUs visible | 2 |
| RAM | Approximately 7.8 GiB |
| Swap usage at recorded check | 0 MB |

Tools used: Python, `psutil`, Bash/Linux CLI, `ps`, `top`, CSV, Git and GitHub Codespaces.

## 6. Repository outputs

After task-wise folder organization, the intended paths are:

```text
Task-02/
├── system_monitor.py
├── system_monitor.csv
└── NOTES.md
```

The implementation and CSV were originally stored under `src/` and `logs/`, then moved into `Task-02/` during repository organization.

## 7. Testing and verification

The following checks were performed:

- Python syntax check with `py_compile`.
- A run configured for 5 samples.
- A run configured for 10 samples.
- Inspection of the generated CSV.
- Independent process/system inspection using `ps` and `top`.
- Git commit and push of the initial implementation.

The initial implementation commit was recorded as `2725a4b`. The later task-folder reorganization may be represented by another commit.

### Suggested repeatable verification

From the repository root:

```bash
python -m py_compile Task-02/system_monitor.py
python Task-02/system_monitor.py
```

Inspect the script's command-line options before supplying optional arguments. If supported, use:

```bash
python Task-02/system_monitor.py --help
```

Inspect the generated log:

```bash
head Task-02/system_monitor.csv
```

## 8. Problem encountered and resolution

**Problem:** A generated `__pycache__` directory appeared as an untracked item after running Python.

**Resolution:** The generated cache directory was removed before checking repository status and committing. Python-generated files should be ignored using `.gitignore`, for example:

```gitignore
.venv/
__pycache__/
*.pyc
```

## 9. Engineering observations and limitations

- CPU and memory values are time-dependent; do not report a single sample as a permanent system characteristic.
- Codespaces is cloud-hosted, so its resource readings describe that environment.
- Process CPU percentages may be sampled differently from system CPU percentages; compare them with their measurement context in mind.
- A system-monitoring script can report CPU and memory metrics, but it does not automatically measure hardware power consumption or temperature.
- Preserve the CSV from the actual test run when documenting exact measurements.

## 10. Outcome

A Python-based system monitoring script and CSV logging workflow were implemented and tested in GitHub Codespaces. The task established basic familiarity with Linux resource metrics, process inspection and repeatable logging.

## 11. Next assigned task

**Task-03 — Sensor Data Ingestion:** create a synthetic sensor-data pipeline that generates raw packets, parses and validates their fields, and separates valid and rejected records.
