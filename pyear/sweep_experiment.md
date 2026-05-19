

## instruction to agent

Conduct a **full Blink Detection benchmark and sweep experiment** on **EAR time series** across:

* **all subjects**
* **all available video segments per subject**
* **all registered blink-detection algorithms**

### 1) Algorithm discovery

All registered algorithms are located in:

`C:\Users\balan\IdeaProjects\pyear\src\detectors`

The agent must:

* automatically discover and load **every registered blink-detection algorithm** from this directory
* build a complete inventory of algorithms before running experiments
* include each algorithm in the experiment map
* fail loudly and log clearly if any detector cannot be imported, initialized, or executed

If the codebase contains registry metadata, use it. Otherwise, infer available detectors programmatically and record the discovery logic in the experiment manifest.

---

### 2) Dataset coverage

Run the experiment on the full dataset.

#### EAR signal path

Pattern:

`D:\dataset\drowsy_driving_raja_processed\<subject>\<video_segment>\seg_data_raw\ear_raw.fif`

Examples:

* `D:\dataset\drowsy_driving_raja_processed\S1\S01_20170519_043933\seg_data_raw\ear_raw.fif`
* `D:\dataset\drowsy_driving_raja_processed\S1\S01_20170519_043933_2\seg_data_raw\ear_raw.fif`
* `D:\dataset\drowsy_driving_raja_processed\S1\S01_20170519_043933_3\seg_data_raw\ear_raw.fif`

Each subject may have up to 3 video segments, but the agent must not assume exactly 3. It must discover all valid segments dynamically.

#### Ground-truth label path

Pattern:

`D:\dataset\drowsy_driving_raja\human_label_annotation\<subject>\<video_segment>\ear_eog.csv`

Examples:

* `D:\dataset\drowsy_driving_raja\human_label_annotation\S1\S01_20170519_043933\ear_eog.csv`
* `D:\dataset\drowsy_driving_raja\human_label_annotation\S1\S01_20170519_043933_2\ear_eog.csv`
* `D:\dataset\drowsy_driving_raja\human_label_annotation\S1\S01_20170519_043933_3\ear_eog.csv`

The agent must pair each EAR file with its matching label file and log any missing or invalid pair.

---

### 3) Subject-specific baseline handling

Some algorithms require subject-specific eye-open / eye-closed baseline values.

Baseline path pattern:

`D:\dataset\drowsy_driving_raja\EC_EC_EAR_output\th_diff_percentage\combined_<subject>.json`

Example:

`D:\dataset\drowsy_driving_raja\EC_EC_EAR_output\th_diff_percentage\combined_S1.json`

Rules:

* baseline files must be used **only for the matching subject**
* calibrated / normalized EAR methods must use the subject-matched baseline when required
* if a detector requires a baseline and none is available, mark that experiment as **invalid / skipped with reason**
* never mix baselines across subjects

---

### 4) Experiment planning requirement

Before running any detector, the agent must first create an **experiment map**.

The experiment map must enumerate, at minimum:

* subject ID
* video segment ID
* EAR signal file path
* ground-truth label path
* baseline file path if applicable
* detector name
* detector version or source fingerprint if available
* parameter search space
* optimization strategy
* evaluation protocol
* output folder
* experiment hash ID
* run status

This experiment map is the source of truth for execution, resume, audit, and result traceability.

---

### 5) Experiment identity and traceability

Each experiment setup must have a **stable hash-based ID**.

The hash must be generated from the canonical experiment configuration, including:

* subject
* segment
* detector
* code fingerprint or detector file signature if possible
* parameter search space definition
* optimization strategy
* objective metric
* evaluation protocol
* baseline usage
* any preprocessing options
* random seed policy

Use this hash as the main experiment identifier in:

* filenames
* output directories
* logs
* checkpoints
* summaries
* resume manifests

This is required so that duplicated or resumed runs remain traceable and unambiguous.

---

### 6) Hyperparameter search policy

If a detector requires finding an optimal parameter set or parameter pair, **do not use brute-force grid search** unless explicitly justified as unavoidable.

Prefer smarter search methods such as:

* **Random search**
* **Bayesian optimization**
* **Successive halving / Hyperband**
* **Evolutionary algorithms**
* **Population-based training**

Guidance:

* use **random search** as a strong default baseline when the space is large or mixed
* use **Bayesian optimization** when objective evaluations are expensive and the search space is well-structured
* use **successive halving / Hyperband** when weak candidates can be discarded early
* use **evolutionary methods** for irregular, conditional, or highly non-convex search spaces
* use **population-based training** only when the detector/training procedure is iterative and supports population-style adaptation

The agent must choose the search strategy based on detector characteristics and compute cost, and record the rationale in the experiment metadata.

For small discrete spaces, exhaustive enumeration is allowed only if it is clearly cheaper and simpler than advanced optimization.

---

### 7) Evaluation requirements

For every detector and every subject/segment combination, evaluate against the provided ground truth.

At minimum, record:

* precision
* recall
* F1-score
* false positives
* false negatives
* detection count
* blink timing overlap / matching stats if supported
* runtime
* parameter values used
* optimization history if tuning was performed

If multiple objective metrics are relevant, choose one primary optimization target and record all secondary metrics.

The optimization target must be explicitly stated in the experiment metadata.

---

### 8) Resume / recovery / takeover requirement

The experiment must be **resumable**.

This is critical because execution may stop unexpectedly due to:

* power failure
* machine shutdown
* API limit
* crash
* manual interruption
* handover to another agent or vendor

The system must support continuing from the last safe point without rerunning completed work unnecessarily.

#### Required resume mechanism

Implement:

1. **checkpointing**

    * persist results after every completed experiment unit
    * a unit should be at least one `(subject, segment, detector, config)` run

2. **run manifest**

    * maintain a machine-readable manifest with status values such as:

        * pending
        * running
        * completed
        * failed
        * skipped
        * invalid

3. **atomic write discipline**

    * avoid corrupting result files during abrupt termination
    * write temporary files first, then rename atomically when complete

4. **resume entrypoint**

    * provide a documented trigger for restart, for example:

        * `--resume`
        * `resume_from_manifest()`
        * `--resume-incomplete`
    * on restart, the system must:

        * load the manifest
        * detect completed experiment hashes
        * skip completed work
        * retry only failed or unfinished units according to policy

5. **takeover instructions**

    * generate a small handover file describing:

        * where the manifest is
        * where logs are
        * how to resume
        * current progress summary
        * failed experiments requiring attention

#### Suggested restart trigger

Use a restart command or equivalent workflow such as:

`python run_blink_sweep.py --resume`

or

`python run_blink_sweep.py --resume-incomplete --manifest <path_to_manifest>`

Also produce a human-readable `HOW_TO_RESUME.md` in the experiment output root.

---

### 9) Logging and live monitoring

Ensure there is a **live logger**.

Requirements:

* real-time console logging
* file logging to persistent log files
* structured logs where possible
* progress reporting at experiment-map level and detector level
* periodic summary of:

    * total experiments
    * completed
    * running
    * failed
    * remaining
    * elapsed time
    * throughput

The live logger should make it easy to see current progress and diagnose failures without opening code.

If practical, also maintain:

* a rolling summary CSV or JSONL
* per-experiment log files
* an aggregate leaderboard file updated incrementally

---

### 10) Compute utilization

The machine is high-spec with a multi-core CPU. The agent should make good use of available compute.

Requirements:

* parallelize independent experiment units
* maximize CPU utilization without destabilizing the machine
* avoid oversubscription
* control worker count explicitly
* separate experiment-level parallelism from algorithm-internal threading
* log CPU worker configuration in the manifest

Recommended approach:

* parallelize across subject/segment/detector/config units
* cap internal BLAS / NumPy / MKL thread counts when needed to avoid worker explosion
* make concurrency configurable, for example:

    * `--n-workers`
    * `--max-parallel-experiments`

The system should default to an efficient setting, but remain safe and reproducible.

---

### 11) Folder-structure documentation

The dataset and experiment folder structure is documented here:

`C:\Users\balan\IdeaProjects\pyear\ear_eog_experiment\planning\folder_structure.md`

Rules:

* read this file before creating new output directories
* if any new folder structure is added, update this file
* keep the documentation aligned with actual output paths
* do not create undocumented folder layouts

---

### 12) Output organization

Create a clean, reproducible output structure for:

* experiment map
* manifests
* logs
* checkpoints
* per-run results
* optimization histories
* aggregate summaries
* final rankings
* failure reports
* resume instructions

All outputs must be tied back to the experiment hash and be understandable without reading source code.

---

### 13) Failure handling

The agent must be robust to partial failures.

If a detector or file pair fails:

* log the error with full context
* mark the corresponding experiment unit as failed
* continue with remaining units unless the failure is fatal to the entire pipeline
* include a failure summary at the end

Do not let one bad detector or one bad segment stop the full sweep.

---

### 14) Reproducibility

Where randomness is used:

* set and record seeds
* record optimization sampler settings
* record software environment details if possible
* record detector source fingerprint or git commit if available

The goal is that another agent can reproduce or audit the same experiment later.

---

### 15) Final deliverables

At the end, produce:

1. **experiment map**
2. **run manifest with statuses**
3. **aggregate results table**
4. **detector ranking summary**
5. **best parameter configuration per detector**
6. **best parameter configuration per subject if relevant**
7. **failure report**
8. **resume instructions**
9. **updated folder_structure.md if new folders were introduced**

---
Important,the agent must follow the skill and requirement mention under
C:\Users\balan\IdeaProjects\pyear\agent-skillbook\skills

in addition, for validation, I also may run vizualization check something similar like in

C:\Users\balan\IdeaProjects\pyear\tutorial\visualize_blink_predictions.py