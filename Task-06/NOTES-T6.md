# Task-06: Acoustic Sensing and TDoA Theory

**Project:** RE-T1 — Embedded AI Training  
**Date:** 10 October 2026  
**Task:** Acoustic Sensing & Time Difference of Arrival (TDoA)

## 1. Objective

The objective of this practical was to understand the basics of acoustic sensing and Time Difference of Arrival (TDoA) using synthetic signals. The practical generated two simulated microphone signals with a known time delay and used cross-correlation to estimate their relative delay.

## 2. Concepts Studied

### Acoustic sensing
Acoustic sensing involves capturing and analyzing sound waves using sensors such as microphones. In a digital system, sound is represented as a sequence of numerical samples.

### Sampling rate
The sampling rate indicates how many samples are taken per second. This practical used a sampling rate of 48,000 Hz, meaning 48,000 samples per second.

### Time Difference of Arrival (TDoA)
TDoA is the difference between the arrival times of a signal at two sensors.

TDoA = t2 − t1

The magnitude of the corresponding path-length difference can be approximated as:

Path difference = speed of sound × absolute TDoA

For this demonstration, the speed of sound was assumed to be 343 m/s.

### Cross-correlation
Cross-correlation compares two signals at different relative shifts. The lag corresponding to the maximum correlation is used to estimate their relative delay.

## 3. Implementation

Two Python scripts were created:

- `acoustic_tdoa_demo.py`: Generates a synthetic 1 kHz sine wave and a delayed copy, then saves signal samples and a comparison plot.
- `acoustic_tdoa_correlation.py`: Generates the synthetic signals, computes cross-correlation, estimates the lag, converts it to time delay, calculates path-length difference magnitude, and saves the result and correlation plot.

The signals represent simulated microphone inputs. No physical microphones or external audio recordings were used.

## 4. Configuration

- Sample rate: 48,000 Hz
- Signal frequency: 1,000 Hz
- Signal duration: 0.05 seconds
- Known simulated delay: 1.000 ms
- Delay in samples: 48
- Assumed speed of sound: 343 m/s

## 5. Results

| Metric | Result |
|---|---:|
| Known delay | 1.000 ms |
| Estimated delay | 1.000 ms |
| Estimated lag | 48 samples |
| Path-length difference magnitude | 0.343 m |

The estimated delay matched the configured synthetic delay for this test case.

## 6. Output Files

- `acoustic_tdoa_demo.py`
- `acoustic_signals.csv`
- `acoustic_signals.png`
- `acoustic_tdoa_correlation.py`
- `tdoa_results.csv`
- `tdoa_correlation.png`

## 7. Limitations

1. The signals were generated synthetically rather than captured using physical microphones.
2. The delay was configured in advance, so this is a controlled simulation rather than validation against an unknown real-world delay.
3. A pure sine wave is periodic and can produce multiple correlation peaks, which can make delay estimation ambiguous.
4. A single TDoA measurement does not generally provide a unique 2D or 3D source location. Sensor geometry and additional measurements are needed.
5. Environmental noise, echoes, microphone synchronization, and sampling accuracy have not been tested.

## 8. Conclusion

This practical demonstrated how to generate synthetic acoustic signals, simulate a relative arrival delay, estimate the delay using cross-correlation, and calculate an approximate path-length difference. The estimated delay was 1.000 ms, corresponding to 48 samples at 48,000 Hz and a path-length difference magnitude of 0.343 m under the assumed sound speed.

The practical provides a foundation for future testing with noisy signals and real microphone data.