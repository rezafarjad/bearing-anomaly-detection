\# Bearing Anomaly Detection



A vibration-analysis project for identifying rolling-bearing fault signatures in

the Case Western Reserve University (CWRU) bearing dataset.



The project uses FFT preprocessing, envelope analysis, and kurtosis-based

resonance-band selection to compare healthy, inner-race, ball, and outer-race

bearing conditions.



\## Results



At approximately 1772 RPM, the expected fault frequencies are:



| Signature | Frequency (Hz) |

|---|---:|

| Shaft rotation | 29.53 |

| Inner race (BPFI) | 159.93 |

| Outer race (BPFO) | 105.87 |

| Ball fault (2×BSF) | 139.20 |



The multi-resolution kurtosis band scan found:



| Condition | Result |

|---|---|

| Normal | No fault-frequency claim |

| Inner race, 0.007 inch | 159.6 Hz, matching BPFI |

| Outer race, 0.007 inch | 106.3 Hz and 212.6 Hz, matching BPFO and its second harmonic |

| Ball, 0.007 inch | No clear 2×BSF signature with the current configuration |



The ball-fault result is reported as unresolved rather than overstated.



\## Methods



1\. Load 12 kHz drive-end accelerometer signals from CWRU data.

2\. Remove the signal mean and apply a Hann window before FFT analysis.

3\. Calculate theoretical bearing frequencies from bearing geometry and RPM.

4\. Use envelope analysis:

&#x20;  - band-pass filter the vibration signal;

&#x20;  - obtain the Hilbert-transform envelope;

&#x20;  - calculate the envelope spectrum;

&#x20;  - compare peaks with fault-frequency theory.

5\. Compare two band-selection approaches:

&#x20;  - Method A: fixed-width spectral-kurtosis-inspired baseline;

&#x20;  - Method B: multi-resolution kurtosis band scan using 250, 500, and 1000 Hz bands.



Method B improved outer-race detection while preserving the strong inner-race

result.



\## Project structure



```text

src/

&#x20; data\_loader.py              Load CWRU MATLAB data

&#x20; theoretical\_frequencies.py  Calculate BPFI, BPFO, BSF, and FTF

&#x20; plot\_fft.py                 FFT analysis

&#x20; envelope\_analysis.py        Envelope-spectrum workflow

&#x20; band\_scan.py                Multi-resolution kurtosis band selection



tests/                        Unit tests

docs/experimental\_protocol.md Scientific method and recorded results

figures/                      Generated comparison plots

