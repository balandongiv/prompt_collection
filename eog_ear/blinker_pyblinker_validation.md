
```text
You are working on a MATLAB-to-Python migration bugfix task.

Goal
Bring pyblinker output into exact agreement with the legacy MATLAB Blinker output on real public-dataset subjects, not just on isolated single-file comparison tests. The target is to reach 100% matching for blink-region detection against the MATLAB/ground-truth blinker output, while keeping the existing comparison tests passing.

High-level context
We are migrating Blinker (MATLAB) into Python as pyblinker.

Current status:
- Logic comparisons on single files appear to pass, as indicated by these tests:
  - test/blinker_pyblinker_comparison/test_a2_stat.py
  - test/blinker_pyblinker_comparison/test_a_get_blink_position.py
  - test/blinker_pyblinker_comparison/test_b_fitblink.py
  - test/blinker_pyblinker_comparison/test_c_BlinkProperties.py
- However, when evaluated on an open public dataset, the result accuracy is not yet 100%.
- The practical issue is that the blink regions detected by legacy Blinker / ground truth do not fully match pyblinker.

Important implementation area
Pay special attention to:
- pyblinker/pipeline_steps.py
- especially process_channel_data(...)

Starter investigation target:
- pyblinker/blinker/get_blink_positions.py
- especially get_blink_position(...)

But do NOT assume the bug is only there. Also consider the full logic under process_channel_data, including:
1. get_blink_position
2. FitBlinks
3. get_blink_statistic
4. get_good_blink_mask
5. BlinkProperties
6. pAVR restriction

Reference function under review
def process_channel_data(detector, channel: str, verbose: bool = True) -> None:
    """Process blink data for a single channel using the legacy six-step pipeline."""
    logger.debug("Processing channel: %s", channel)

    # STEP 1: Get blink positions
    df = get_blink_position(
        detector.params,
        blink_component=detector.raw_data.get_data(picks=channel)[0],
        ch=channel,
    )

    if df.empty and verbose:
        logger.warning("No blinks detected in channel: %s", channel)

    # STEP 2: Fit blinks
    fitblinks = FitBlinks(
        candidate_signal=detector.raw_data.get_data(picks=channel)[0],
        df=df,
        params=detector.params,
    )
    fitblinks.dprocess()
    df = fitblinks.frame_blinks

    # STEP 3: Extract blink statistics extractBlinkProperties.m
    # Calculate an amplitude criterion (frames in blink to those out) and Now calculate the cutoff ratios -- use default for the values
    blink_stats = get_blink_statistic(
        df,
        detector.params["z_thresholds"],
        signal=detector.raw_data.get_data(picks=channel)[0],
    )
    blink_stats["ch"] = channel
    # There is a step for << Reduce the number of candidate signals based on the blink amp ratios >>, but we move it to channel selection step.

    # STEP 4: Get good blink mask extractBlinkProperties.m
    _, df = get_good_blink_mask(
        df,
        blink_stats["best_median"],
        blink_stats["best_robust_std"],
        detector.params["z_thresholds"],
    )
    # What happen if no good blinks are found or all blinks are bad?
    if df.empty and verbose:
        logger.warning("No good blinks found in channel: %s", channel)
        return
    # STEP 5: Compute blink properties
    df_in = df.copy()
    df_out = BlinkProperties(
        detector.raw_data.get_data(picks=channel)[0],
        df_in,
        detector.params["sfreq"],
        detector.params,
    ).df

    # STEP 6: Apply pAVR restriction # Suggest to move up to df_out = df_out[~(condition_1 & condition_2)] into a specific function.
    condition_1 = df_out["pos_amp_vel_ratio_zero"] < detector.params["p_avr_threshold"]
    condition_2 = df_out["max_value"] < (
        blink_stats["best_median"] - blink_stats["best_robust_std"]
    )
    df_out = df_out[~(condition_1 & condition_2)]

    detector.all_data_info.append({"df": df_out, "ch": channel})
    detector.all_data.append(blink_stats)

Available MATLAB references
You will be given the actual MATLAB implementation.
Additional references:
- test/blinker_pyblinker_comparison/matlab_fitblink
- full MATLAB code may also be referenced from:
  D:\code development\matlab_plugin\eeglab2025.1.0\plugins\Blinker1.2.0

MATLAB execution support
You may use MATLAB Engine API for Python if needed.
Use it when direct code reading is insufficient, especially to:
- run the MATLAB implementation on exactly the same input
- compare intermediate outputs step by step
- inspect where divergence first appears

Primary task
Find the source of mismatch between MATLAB Blinker and pyblinker on real subjects, fix the Python code, and validate progressively until the matching reaches 100% or until the precise blocking issue is identified with strong evidence.

Required working style
Do not make broad speculative rewrites.
Work incrementally, with evidence at every step.

Validation strategy
Because the dataset is large, use this rollout strategy:
1. Start with the best first subjects first.
2. If results improve and remain stable, then proceed with two subjects.
2. If results improve and remain stable, expand to 5 subjects.
3. If still good, slowly increase the number of subjects.
4. Only scale further when the previous stage is clearly understood and documented.

Subject list location
- blinker_pyblinker_validation/summary_metrics.csv

Important note:
- The CSV is already sorted descending by share_within_tolerance_percent.
- Use that ordering when selecting the first 2, then 5, then more subjects.

Metric/evaluation script
Use:
- blinker_pyblinker_validation/blink_compare_from_csv.py

Track these metrics at minimum:
- share_within_tolerance_percent
- precision_strict
- recall_strict
- f1_strict
- accuracy_strict
- precision_lenient
- recall_lenient
- f1_lenient
- accuracy_lenient

Core debugging approach
Your job is not just to make metrics go up. Your job is to identify the first point of divergence between MATLAB and Python and fix it correctly.

Preferred investigation order
1. Reproduce the mismatch on the top 2 subjects.
2. Identify where pyblinker first diverges from MATLAB:
   - blink candidate positions
   - fitted blink boundaries
   - blink statistics
   - good-blink masking
   - blink property extraction
   - pAVR filtering
3. Compare intermediate artifacts step by step, not just final metrics.
4. For each suspected stage:
   - compare inputs
   - compare outputs
   - compare thresholds/constants
   - compare indexing conventions
   - compare edge-case behavior
   - compare rounding / casting / dtype behavior
   - compare inclusive vs exclusive boundaries
   - compare NaN / empty-frame handling
   - compare sampling-frequency assumptions
5. Fix the smallest correct thing first.
6. Re-run:
   - focused unit tests
   - comparison tests
   - subject-level validation
7. Only move to broader subject counts after documenting the result.

Things to specifically watch for
- MATLAB 1-based vs Python 0-based indexing
- inclusive/end-boundary differences
- off-by-one region width issues
- integer rounding vs floor/ceil/round behavior
- handling of empty detections
- signal slicing differences
- pandas filtering side effects
- DataFrame copy vs view mutation
- sorting stability / row-order assumptions
- threshold interpretation differences
- z-threshold use
- channel-specific behavior
- pAVR filter interaction with earlier steps
- any silent type coercion
- median / robust std implementation differences
- whether candidate blink frames are altered before later filtering
- differences hidden by single-file tests but exposed in multi-subject/public-data runs

Deliverables for every code change
For every change you make, record it in a markdown file with a proper descriptive name.

Why:
If the experiment stops midway, we must be able to resume from the recorded history and avoid repeating the same plan.

Logging requirements
Create a new markdown log for each meaningful investigation or fix attempt.
Use a clear filename, for example:
- blinker_pyblinker_validation/finding/001_get_blink_position_boundary_check.md
- blinker_pyblinker_validation/finding/002_fitblink_window_alignment.md
- blinker_pyblinker_validation/finding/blinker_migration_fix_003_pavr_mask_order.md

Each markdown record must include:
1. Title
2. Date/time
3. Hypothesis
4. Files inspected
5. Files changed
6. Exact change made
7. Why the change was made
8. MATLAB reference used
9. Validation scope
   - which subjects
   - how many subjects
   - which tests
10. Before/after metrics
11. Whether the change was kept or reverted
12. Next recommended step

Do not skip the markdown log, even for failed ideas.
Failed hypotheses are useful and must be recorded.

Working rules
- Preserve existing passing comparison tests unless there is strong evidence that the tests themselves encode wrong assumptions.
- Prefer minimal, targeted fixes over refactors.
- If you refactor for clarity, do it only after proving behavior stays equivalent.
- If you cannot prove a fix is correct, do not present it as final.
- If MATLAB and Python differ, trust MATLAB behavior unless there is documented evidence that the MATLAB path is buggy and the project explicitly wants to change it.
- Keep all experiments reproducible.

Suggested concrete plan
Phase 1: Baseline
- Run the current comparison tests.
- Run validation on the top 2 subjects from summary_metrics.csv using blink_compare.py.
- Save the baseline metrics.

Phase 2: First divergence analysis
- Inspect get_blink_position first.
- Compare MATLAB vs Python intermediate outputs for the same top 2 subjects.
- If needed, instrument both sides to dump intermediate blink positions and boundaries.

Phase 3: Downstream stage analysis
If get_blink_position is not the source, continue in order through:
- FitBlinks
- get_blink_statistic
- get_good_blink_mask
- BlinkProperties
- pAVR restriction

Phase 4: Fix + verify
- Implement the smallest justified fix.
- Re-run:
  - targeted unit tests
  - comparison tests
  - top 2 subjects

Phase 5: Controlled scaling
- If top 2 subjects are good, move to top 5 subjects.
- If top 5 are good, increase gradually.

Expected output format from you after each iteration
After each investigation/fix iteration, report:
1. What was investigated
2. What divergence was found
3. What files were changed
4. What markdown log file was created
5. Test results
6. Subject-validation results
7. Whether the change is retained
8. The next most likely place to investigate

Definition of done
The task is considered done only when:
- pyblinker matches MATLAB/ground-truth blink regions at 100% for the validated scope, and
- the relevant tests pass, and
- the investigation/fix history is documented in markdown logs.

If full 100% is not yet reached, do not stop with vague conclusions.
Instead, provide:
- the exact remaining mismatch pattern
- the most likely root cause
- the evidence collected
- the next prioritized debugging step

Start now with:
1. establishing a reproducible baseline on the top 2 subjects from blinker_pyblinker_validation/summary_metrics.csv by running conda run -n pyblinker python -m pyblinker.blinker_pyblinker_validation.blink_compare_from_csv.py
or C:\Users\balan\anaconda3\condabin\conda.bat run -n pyblinker python -m blinker_pyblinker_validation.blink_compare_from_csv
2. investigating get_blink_position first
3. creating the first markdown investigation log before or alongside the first code change
```
