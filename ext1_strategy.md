# Subject-Independent EEG-to-Fatigue Classification Strategy

To ensure **subject-wise GroupKFold** in this new Experiment 1, treat **subject ID as the grouping key** and treat **PERCLOS as the external binary label** for each epoch.

## Table of Contents
1. [Define the Unit of Analysis First](#1-define-the-unit-of-analysis-first)
2. [Compute PERCLOS per Epoch](#2-compute-perclos-per-epoch)
3. [Ensure Subject-Wise GroupKFold](#3-ensure-subject-wise-groupkfold)
4. [What Must Happen Inside Each Fold](#4-what-must-happen-inside-each-fold)
5. [What is Allowed Before CV](#5-what-is-allowed-before-cv)
6. [Best Interpretation of Experiment 1 Now](#6-best-interpretation-of-experiment-1-now)
7. [How to Structure the Binary Experiment](#7-how-to-structure-the-binary-experiment)
8. [Recommended Label Construction Details](#8-recommended-label-construction-details)
9. [Strong Practical Pipeline](#9-strong-practical-pipeline)
10. [Recommended Models](#10-recommended-models)
11. [Best Feature-Testing Strategy](#11-best-feature-testing-strategy)
12. [Common Mistake to Avoid](#12-common-mistake-to-avoid)
13. [A Concise Paper-Ready Wording](#13-a-concise-paper-ready-wording)
14. [Minimal Implementation Template](#14-minimal-implementation-template)
15. [Bottom Line](#15-bottom-line)

---

The clean version of your experiment is:

* **Input**: EEG PSD features by region/channel
* **Target Label**: Binary fatigue label from PERCLOS
* **CV Rule**: All epochs from one subject must stay in only one fold (Subject-Independent)

This framing makes Experiment 1 a **subject-independent EEG-to-fatigue classification** problem.

## 1. Define the Unit of Analysis First

Your sample should be an **epoch**, for example:

* 30 s epoch, or
* 60 s epoch

For every epoch, build one row containing:

* `subject_id`
* `epoch_id`
* EEG PSD features
* PERCLOS value from `ear_eog.csv`
* Binary fatigue label from PERCLOS

The resulting table structure should look like:

`[subject_id, epoch_id, occ_delta, occ_theta, frontal_alpha, ..., perclos, y_binary]`

---


## 2. Compute PERCLOS per Epoch

Eye closure was defined using a **subject-specific EAR threshold** obtained from the EO/EC calibration file at the **60% threshold setting**. For example, for Subject 1, the file `D:\dataset\drowsy_driving_raja\EC_EC_EAR_output\th_diff_percentage\combined_S1.json` provides:

* `overall_ear_threshold = 0.15701501188446093`
Say, for subject 1, the `ear_raw.fif` which contains the EAR signal under `D:\dataset\drowsy_driving_raja_processed\S1\S01_20170519_043933\seg_data\ear_raw.fif` with a sampling rate of 30 Hz, was segmented into 30 s epochs. Each epoch contains 900 samples (30 s * 30 Hz). Each sample has an EAR value.
* 
This means that, for Subject 1, any frame with:

$$
EAR < 0.15701501188446093
$$

was treated as an **eye-closed** sample.

After converting each frame into open-eye or closed-eye status, **epoch-level PERCLOS** was computed as the proportion of time within that epoch during which the eyes were closed. The PERCLOS was calculated as the total closed-eye duration within the epoch divided by the epoch length:

$$
\text{PERCLOS}_e = \frac{\text{closed-eye time in epoch } e}{\text{epoch length}}
$$

A binary fatigue label was then assigned from the epoch-level PERCLOS value. If fatigue was operationalized as **more than 80% eye closure within an epoch** (to be consistent with subsequent sections), the label for epoch $e$ was defined as:

$$
y_e =
\begin{cases}
1, & \text{if PERCLOS}_e > 0.80 \\
0, & \text{otherwise}
\end{cases}
$$

where:

* $y_e = 0$ indicates **alert / non-fatigue**
* $y_e = 1$ indicates **fatigue**

A key distinction is that the **60% setting** was used to determine the **subject-specific EAR closure threshold**, and the **80% cutoff** was used to assign the **binary fatigue label** from the epoch-level PERCLOS value.




## 3. Ensure Subject-Wise GroupKFold

This is the critical part. You must use:

* `groups = subject_id`
* `X = EEG PSD features`
* `y = binary PERCLOS label`

In scikit-learn terms:

```python
from sklearn.model_selection import GroupKFold

gkf = GroupKFold(n_splits=5)

for train_idx, test_idx in gkf.split(X, y, groups=subject_ids):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    subj_train, subj_test = subject_ids[train_idx], subject_ids[test_idx]
```

The key check is to ensure no subject leakage exists:

```python
assert set(subj_train).isdisjoint(set(subj_test))
```

If that assertion passes for every fold, then there is no subject leakage.

## 4. What Must Happen Inside Each Fold

Even if the PERCLOS label is already fixed, everything learned from EEG features must be fit on training subjects only.

Inside each fold:

1. Split by subject.
2. Fit the imputer on `X_train` only.
3. Fit the scaler on `X_train` only.
4. Fit the feature selector on `X_train` only.
5. Train the classifier on `X_train`.
6. Apply transforms to `X_test`.
7. Evaluate on unseen subjects.

**Do not:**

* Normalize using all subjects.
* Select top PSD features using all subjects.
* Remove channels based on all-subject statistics before CV.

Doing so would reintroduce data leakage.

## 5. What is Allowed Before CV

These operations are usually safe before CV because they do not learn from the full EEG dataset in a target-leaking way:

* Segmenting epochs.
* Extracting PSD per epoch.
* Computing per-epoch PERCLOS from manual blink coverage.
* Assigning the binary label using the fixed 60% rule.

**What is NOT safe before CV:**

* Feature scaling using all epochs.
* PCA using all epochs.
* Selecting top channels by correlation with labels using all epochs.
* Tuning thresholds from the full dataset.

## 6. Best Interpretation of Experiment 1 Now

With this setup, Experiment 1 becomes:

> *Can EEG PSD features, especially occipital spectral power, classify binary fatigue states defined independently by PERCLOS, under subject-independent evaluation?*

That is cleaner than saying EEG defines the label. Here, **PERCLOS is the ground-truth label**, and **EEG PSD is the predictor**.

## 7. How to Structure the Binary Experiment

For each epoch length, run a separate experiment to determine which gives better subject-independent EEG fatigue detection:

### Experiment 1A
* 30 s epochs
* Binary PERCLOS label
* GroupKFold by subject

### Experiment 1B
* 60 s epochs
* Binary PERCLOS label
* GroupKFold by subject

Then compare the following metrics:
* Balanced Accuracy
* Macro F1-Score
* AUROC
* Confusion Matrix

## 8. Recommended Label Construction Details

Because your PERCLOS is based on blink/closure coverage intervals, be explicit in the paper:

* PERCLOS is computed per epoch from the manual blink coverage ratio in `ear_eog.csv`.
* An epoch is labeled fatigue if closure coverage exceeds 60%.
* This binary behavioral label is used as the target for EEG PSD classification.

This wording is strong and unambiguous.

## 9. Strong Practical Pipeline

A robust pipeline involves:

1. Segmenting the session into 30 s or 60 s epochs.
2. Extracting EEG PSD features by region/channel.
3. Computing epoch-level PERCLOS from `ear_eog.csv` blink-coverage intervals.
4. Assigning the binary label using the 60% threshold.
5. Running `GroupKFold` with `groups = subject_id`.
6. Within each fold, fitting preprocessing and the model on training subjects only.
7. Testing on held-out subjects only.
8. Summarizing fold-wise performance.

## 10. Recommended Models

For this experiment, start with simple interpretable models:

* Logistic Regression
* Linear SVM
* Random Forest (as a nonlinear comparison)

If you want feature discovery, **Elastic Net Logistic Regression** is an excellent main model. It helps identify whether:
* Occipital delta alone works.
* The whole occipital region works best.
* Additional bands improve prediction.

## 11. Best Feature-Testing Strategy

Since your stated hypothesis is about occipital PSD, evaluate it in stages to show whether the simplest occipital hypothesis is enough before moving to complex models:

* **Stage 1**: Occipital delta only
* **Stage 2**: Occipital delta + other occipital bands
* **Stage 3**: All regional PSD features
* **Stage 4**: Channel-level PSD features

## 12. Common Mistake to Avoid

A very common mistake that inflates performance:

* Computing all epochs.
* Randomly splitting epochs.
* Training and testing on mixed subjects.

The model sees the same subject in both sets, which is invalid. The fix is always to **split by `subject_id`, not by epoch**.

## 13. A Concise Paper-Ready Wording

You can describe the method in your paper like this:

> Each driving session was segmented into fixed-length epochs of 30 s or 60 s. For each epoch, EEG PSD features were extracted at both the regional and channel levels. A binary behavioral fatigue label was assigned using the epoch-level PERCLOS value derived from the manual blink coverage ratio in `ear_eog.csv`, with epochs exceeding 60% closure labeled as fatigue. Subject-independent evaluation was enforced using GroupKFold cross-validation, where all epochs from the same subject were assigned to a single fold to prevent subject leakage. All preprocessing, feature selection, and model fitting steps were performed using training subjects only.

## 14. Minimal Implementation Template

```python
import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score

# Assume predefined variables:
# X: EEG PSD features, shape [n_epochs, n_features]
# perclos: epoch-level PERCLOS in [0, 1]
# subject_ids: subject id for each epoch

y = (perclos > 0.60).astype(int)

gkf = GroupKFold(n_splits=5)

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=2000))
])

baccs, f1s = [], []

for train_idx, test_idx in gkf.split(X, y, groups=subject_ids):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    subj_train, subj_test = subject_ids[train_idx], subject_ids[test_idx]

    # Ensure no subject leakage
    assert set(subj_train).isdisjoint(set(subj_test))

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    baccs.append(balanced_accuracy_score(y_test, y_pred))
    f1s.append(f1_score(y_test, y_pred))

print(f"Balanced Accuracy: {np.mean(baccs):.4f}")
print(f"F1 Score: {np.mean(f1s):.4f}")
```

# Execution

use the conda environment `blinker_pyblinker_validation` which alredy dependecies installed.

# Experiment Output
All output should be saved in `D:\dataset\drowsy_driving_raja_processed\data\experimentation\exp1_reconfirm_psd_classification_perclos\<hash>` where `<hash>` is a unique identifier for this experiment run,

# Write a report
After running the experiment, write a report detailing about the experiment design, results, and interpretation in `writing/result/experiment1a.tex`

# Skill
When developing the code, use the skill in agent_skillbook/skills to write modular, reusable code.

For long experiment, it is compulsory to obey `agent_skillbook/skills/experiment-runbook-discipline` and save this in the `D:\dataset\drowsy_driving_raja_processed\data\experimentation\exp1_reconfirm_psd_classification_perclos\<hash>` where `<hash>`

# Folder structure
```powershell
planning/folder_structure.md
```
