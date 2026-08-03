\# Experimental Protocol



\## 1. Project goal



This project investigates whether vibration-signal processing can identify

bearing faults in the Case Western Reserve University (CWRU) dataset.



The main question is:



> Can envelope analysis reveal frequency signatures associated with inner-race,

> outer-race, and rolling-element defects?



The project will compare healthy and faulty bearing signals under the same

approximately 1 hp operating condition.



\## 2. Dataset



\- Dataset: CWRU bearing dataset

\- Measurement channel: drive-end accelerometer

\- Sampling frequency: 12,000 Hz

\- Operating condition: approximately 1 hp

\- Shaft speed: approximately 1772 RPM

\- Classes analysed:

&#x20; - Normal

&#x20; - Inner-race fault, 0.007 inch

&#x20; - Ball fault, 0.007 inch

&#x20; - Outer-race fault, 0.007 inch



The raw vibration signals are stored locally in `data/raw/` and are not

committed to Git because dataset files are large and can be downloaded again.



\## 3. Bearing-fault theory



A local defect creates a repeated mechanical impact whenever a rolling element

passes over it. Each impact can excite high-frequency resonance in the bearing

housing. The impacts repeat at a characteristic frequency determined by bearing

geometry and shaft speed.



The shaft rotation frequency is:



fr = RPM / 60 = 1772 / 60 = 29.53 Hz



Expected characteristic frequencies are:



| Signature | Meaning | Expected frequency (Hz) |

|---|---|---:|

| fr | Shaft rotation frequency | 29.53 |

| BPFI | Inner-race defect frequency | 159.93 |

| BPFO | Outer-race defect frequency | 105.87 |

| BSF | Ball-spin frequency | 69.60 |

| 2×BSF | Common ball-fault signature | 139.20 |

| FTF | Cage frequency | 11.76 |



A fault result is supported when a peak appears near the expected frequency,

its harmonics, or related sidebands.



\## 4. Signal-processing methods



\### 4.1 FFT baseline



The FFT converts the vibration signal from time-domain samples into frequency

components.



Before calculating the FFT:



1\. Remove the mean to eliminate DC offset.

2\. Apply a Hann window to reduce spectral leakage.

3\. Calculate the one-sided amplitude spectrum.



This baseline shows the overall frequency content but may not clearly reveal

bearing impacts.



\### 4.2 Envelope analysis



Envelope analysis is used because bearing impacts often excite high-frequency

resonance while the actual impact repetition rate is much lower.



Procedure:



1\. Select a high-frequency band containing impulsive resonance.

2\. Apply a band-pass filter.

3\. Calculate the Hilbert-transform envelope.

4\. Calculate the FFT of the envelope.

5\. Compare envelope-spectrum peaks with BPFI, BPFO, and 2×BSF.



\### 4.3 Band-selection methods to compare



Method A: current baseline heuristic



\- Calculate STFT magnitude across time.

\- Calculate an excess-kurtosis-like value for each frequency bin.

\- Select a fixed-width 1000 Hz band around the strongest valid candidate.

\- Perform envelope analysis in that band.



This is a useful experimental baseline, but it is not a formal Fast Kurtogram.



Method B: Fast Kurtogram or an equivalent validated kurtogram method



\- Search multiple centre frequencies and bandwidths.

\- Select the frequency band that best highlights transient impacts.

\- Perform envelope analysis using that selected band.



This method will be implemented or reproduced only after Method A is documented

and evaluated fairly.



\## 5. Evaluation rules



For each signal class:



1\. Record the selected band.

2\. Record the strongest envelope-spectrum peaks.

3\. Compare those peaks with theoretical fault frequencies.

4\. Report the distance between an observed peak and its expected frequency.

5\. Check for harmonics and shaft-frequency sidebands.

6\. Compare results with the Normal signal.



A peak is not called a fault signature simply because it is large. It must have

a physically meaningful relationship to the expected characteristic frequency.



\## 6. Current findings



\### Inner-race fault



The envelope spectrum contains a strong peak at 159.6 Hz.



\- Theoretical BPFI: 159.93 Hz

\- Observed peak: 159.6 Hz

\- Interpretation: strong agreement with the inner-race fault frequency



A peak near 319 Hz also agrees with approximately twice BPFI.



\### Ball fault



The current baseline method mainly identified shaft-related frequencies near

29.5 Hz and its harmonics. The expected 2×BSF signature near 139.2 Hz was not

among the strongest reported peaks.



Interpretation: the present selected band does not yet provide strong evidence

for ball-fault identification.



\### Outer-race fault



The current baseline method did not identify a clear dominant peak near BPFO,

which is approximately 105.87 Hz.



Interpretation: the present selected band does not yet provide strong evidence

for outer-race-fault identification.

### Method B: multi-resolution kurtosis band scan

| Class | Selected band (Hz) | Expected signature (Hz) | Key observed peak (Hz) | Interpretation |
|---|---:|---:|---:|---|
| Normal | 625–875 | None | No relevant fault peak | Healthy reference |
| Inner race | 4000–5000 | BPFI: 159.93 | 159.6 | Strong agreement |
| Ball | 5250–5500 | 2×BSF: 139.20 | No clear match | Not identified |
| Outer race | 4500–5500 | BPFO: 105.87 | 106.3, 212.6 | Strong BPFO and second harmonic evidence |

Method B improved outer-race detection compared with Method A. Both methods
identified the inner-race signature. Neither method established a clear ball-fault
signature for this specific recording and configuration.



\## 7. Next steps



1\. Commit this protocol to Git.

2\. Add a repeatable comparison table for all four signal classes.

3\. Validate the current baseline band-selection method.

4\. Implement and validate a proper Fast Kurtogram comparison method.

5\. Compare methods using the same data and fault-frequency criteria.

6\. Build anomaly-detection features only after the signal-processing method is

&#x20;  justified by the results.



\## 8. Scientific references



\- Antoni, J. and Randall, R. B. (2006). The spectral kurtosis: application to

&#x20; the vibratory surveillance and diagnostics of rotating machines.

\- Antoni, J. (2007). Fast computation of the kurtogram for the detection of

&#x20; transient faults.

\- CWRU Bearing Data Center: bearing geometry and drive-end fault data.


### Baseline results table

| Class | Selected band (Hz) | Expected signature (Hz) | Key observed peak (Hz) | Interpretation |
|---|---:|---:|---:|---|
| Normal | 1609–2609 | None | 447.9 | No fault-frequency claim |
| Inner race | 1000–2000 | BPFI: 159.93 | 159.6 | Strong agreement |
| Ball | 4422–5422 | 2×BSF: 139.20 | No clear match | Dominated by shaft harmonics |
| Outer race | 531–1531 | BPFO: 105.87 | No clear match | Not identified by baseline |

