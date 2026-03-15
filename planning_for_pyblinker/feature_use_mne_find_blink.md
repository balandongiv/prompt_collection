Design & Implementation Plan

1. Architectural Approach & Interface:
   We introduce a strategy pattern by adding a pipeline argument to the BlinkDetector constructor, defaulting to "legacy". If "mne" is provided, the detector routes the execution to the new logic instead of
   using the traditional process_all_channels loop. This avoids entangling the new flow with the complex six-step legacy code while providing users a very clean, unified API.

2. Where the Code Lives:
- `pyblinker/blinker/mne_pipeline.py`: The core orchestration module mapping MNE's find_eog_events directly to the BlinkProperties shape calculations.

3. Data Transformation for `BlinkProperties`:
   MNE's find_eog_events detects peak sample indices, but BlinkProperties expects start and end margins (outer_start, outer_end) as well as boundary zero-crossings (left_zero, right_zero, left_base,
   right_base).
- We expand a configurable window (e.g., ±0.3s) around each MNE peak to form generic baseline boundaries.
- We utilize the existing left_right_zero_crossing and create_left_right_base utilities to geometrically construct boundaries around those MNE peaks dynamically.
- We skip the complex iterative fitting step entirely by running BlinkProperties(..., fitted=False).

4. Reused Pipeline Parts:
- BlinkProperties directly computes waveform characteristics using MNE's events.
- left_right_zero_crossing and create_left_right_base are reused from pyblinker.segmentation.geometry to reliably feed BlinkProperties the boundary shapes it needs without FitBlinks.
- detector.create_annotations formatting logic.

5. Testing Strategy:
- A new file test/test_mne_pipeline.py uses unittest to ensure pipeline="mne" successfully initializes, identifies events using EOG/EEG channels via MNE's algorithms, constructs valid boundary
  DataFrames, and produces mne.Annotations.
- A new interactive tutorial script tutorial/01b_mne_usage.py has been built mimicking 01a_basic_usage.py, and it illustrates both pipelines.

  ---

Implementation Details

I have completed the implementation based on the plan above and committed the changes to your local branch:

1. `pyblinker/blinker/mne_pipeline.py`: Created this module to orchestrate the simplified flow: running mne.preprocessing.find_eog_events over the raw signal (which dynamically identifies an EOG
   channel, or falls back to an explicit channel), bounding the resulting peak locations into BlinkProperties-compatible DataFrame format, and resolving geometric bases (left_right_zero_crossing,
   create_left_right_base) right before extracting property metrics with fitted=False.
2. `pyblinker/blinker/pyblinker.py`: Modified the BlinkDetector class to parse the new pipeline argument and seamlessly call get_mne_blink(...) directly instead of falling down to the legacy six-step
   core_get_blink.
3. `tutorial/01b_mne_usage.py`: Written a comprehensive usage example comparing the execution of BlinkDetector(pipeline="legacy") and BlinkDetector(pipeline="mne") side-by-side using the
   mne.datasets.sample dataset. The script plots the new MNE results at the end.
4. `test/test_mne_pipeline.py`: Added a dedicated unittest pipeline to verify df_out structure, shape validity, and functional annotations over standard raw segments. It passed successfully.