
## Goal



**Goal:** evaluate whether blink features extracted from EOG and EEG ocular activity using the pyblinker, can discriminate PSD-defined fatigue states that is extracted from mne-features, where fatigue labels are obtained by clustering EEG PSD patterns into 2, 3, or 4 groups.


## Best strategy list for your exact setup

### 1. Build labels from PSD only, never from blink features

This is very important.

Use PSD features,extracted from mne-features, to create the class labels (via k-means clustering) that define the fatigue states.:


* binary
* 3-class
* 4-class

Then train classifiers using:

* EOG blink features only
* EEG-ocular blink features only
* combined blink features

Then use blink features to predict those PSD-defined classes.

This keeps the validation clean:

* PSD defines the fatigue state
* blink features try to predict it


---

### 2. Do clustering inside training folds only

Since labels come from K-means, you should be careful about leakage.

Best practice:

* split subjects first
* on the training subjects, fit K-means using PSD
* assign cluster labels on training data
* map test samples to the nearest learned centroids
* then evaluate blink-feature classification on those train/test labels

This is much cleaner than clustering all data first.

If you cluster all subjects before CV, the test set influences the label structure.

---

### 3. Use subject-wise cross-validation

Since we have many subjects, use:

* **GroupKFold**
* maybe **StratifiedGroupKFold** if class balance matters and available in your setup

Group = subject ID

This is essential because blink patterns are person-specific.

---

### 4. Treat 2-class, 3-class, and 4-class as separate experiments

Do not mix them into one result.

Report them separately:

* Experiment 2A: binary fatigue state
* Experiment 2B: 3-level fatigue state
* Experiment 2C: 4-level fatigue state

This is useful because:

* binary is easier and more stable
* 3-class may be more realistic
* 4-class may capture finer fatigue levels but is harder

Often the best scientific story is:

* binary gives strongest separability
* multiclass shows whether blink markers scale to finer fatigue gradation

---

### 5. Compare 30 s vs 60 s epochs explicitly

This should absolutely be part of the design.

Good rationale:

* **30 s** gives more samples and may capture shorter-term blink changes
* **60 s** gives more stable PSD and blink statistics

So run both and compare:

* classification performance
* feature stability
* region/channel ranking stability

A likely outcome is:

* 60 s more stable
* 30 s more temporally sensitive

That itself is an important result.

---

### 6. Use simple, interpretable classifiers first

Because we want the best features, not only the best score.

Start with:

* Logistic Regression / multinomial logistic regression
* Linear SVM
* Elastic Net logistic regression

Then optionally compare:

* Random Forest
* XGBoost / LightGBM

For publication, the strongest main model is usually:

* sparse linear model
  because you can interpret selected features

---

### 7. Use feature selection inside each training fold

Since we have many thousands of features, feature selection is necessary.

Several strategy are:

* variance filtering
* correlation filtering
* univariate ANOVA or mutual information
* Elastic Net / L1 feature selection
* stability selection

Recommended order:

1. low variance removal
2. remove near-duplicate/highly correlated features
3. train-fold-only feature selection
4. classifier

Never select features before subject split.

---

### 8. Keep region-level and channel-level analysis separate

Do this in two stages.

#### Stage 1: region level

Group PSD into:

* frontal
* central
* parietal
* occipital
* temporal

Use this first because it is cleaner and easier to interpret.

#### Stage 2: channel level

After region-level analysis, repeat for individual channels.

This avoids a huge multiple-comparison problem too early.


---

### 11. Use dimensionality reduction mainly for comparison, not as main evidence

You can include:

* PCA
* PLS-DA
* maybe LDA projection

But for our main conclusion, it is better to rely on:

* selected original blink features
* interpretable engineered blink features

Because our aim is to say which blink features are fatigue markers.

PCA components are harder to interpret.

A good compromise:

* use PCA/PLS as an auxiliary comparison
* use sparse feature selection as the main result

---

### 12. Evaluate with class-balanced metrics

Since cluster classes may be imbalanced, do not report accuracy alone.

Use:

* balanced accuracy
* macro F1
* weighted F1
* confusion matrix
* one-vs-rest AUROC if appropriate
* Cohen's kappa if helpful

For multiclass, macro F1 is especially useful.

---

### 13. Check cluster validity before classification

Because your labels come from K-means, you should prove the clusters are meaningful.

For each of 2, 3, 4 clusters, report:

* silhouette score
* Davies-Bouldin index
* Calinski-Harabasz index
* class sizes
* whether centroid ordering corresponds to plausible fatigue progression

This is very important. Otherwise reviewers may ask whether the classes are arbitrary.

---

### 14. Order the clusters meaningfully

After K-means, clusters have arbitrary labels.

You should reorder clusters according to fatigue-related PSD pattern, for example using:
* delta
* higher theta
* lower alpha
* theta/alpha ratio
* other known fatigue-related spectral trend

Then label them consistently:

* class 0 = alert
* class 1 = mild fatigue
* class 2 = moderate fatigue
* class 3 = severe fatigue

Without this, multiclass interpretation is weak.

---

### 15. Use stability of selected blink features as a main criterion

Since you want the best features, define “best” as features that:

* are repeatedly selected across folds
* work across subjects
* work in 30 s and 60 s epochs
* work in binary and multiclass settings
* appear in both EOG and EEG-ocular pipelines if possible

This is better than choosing features from a single best-performing fold.

A very strong output table would be:

* feature name
* feature family
* selected frequency across folds
* selected in 30 s?
* selected in 60 s?
* selected in binary?
* selected in 3-class?
* selected in 4-class?
* EOG / EEG / both

That gives you a robust shortlist.

---

## Best practical experiment design

I would suggest this exact structure:

### Experiment 2A: Binary PSD-defined fatigue

* create 2 clusters from training PSD
* classify with blink features
* compare 30 s and 60 s
* compare EOG vs EEG-ocular vs combined

### Experiment 2B: 3-class PSD-defined fatigue

Same setup.

### Experiment 2C: 4-class PSD-defined fatigue

Same setup.

For each:

* region-level first
* channel-level second
* report stable top blink features

---

## Best model pipeline

For each fold:

1. split by subject
2. compute PSD-based labels on training set with K-means
3. assign test labels using training centroids
4. extract blink features for train/test
5. preprocess train only:

    * impute
    * scale
    * low variance removal
    * correlation filtering
6. feature selection on training only:

    * Elastic Net or L1
7. train classifier
8. evaluate on held-out subjects

That is a solid pipeline.

---

## Recommended model comparisons

Keep it manageable. Use maybe 3 main classifiers:

* multinomial logistic regression with Elastic Net
* linear SVM
* Random Forest or gradient boosting as nonlinear comparison

This is enough.

---

## Strongest feature-discovery strategy for your case

For your exact setup, I would prioritize:

### Main

* **Elastic Net multinomial logistic regression**
* because it handles correlated features and gives sparse selection

### Support

* **stability selection across GroupKFold folds**
* to identify robust blink markers

### Optional comparison

* **PLS-DA or PCA + classifier**
* to test whether latent compressed blink features outperform raw blink features

---

## What to say about 30 s vs 60 s

A good interpretation is:

* 30 s epochs may better capture transient blink changes but may produce noisier PSD estimates
* 60 s epochs may provide more stable spectral and blink summaries, potentially improving class separability
* therefore both epoch lengths should be compared empirically

That is a strong justification.

---

## One important caution

Because your labels come from unsupervised clustering, avoid saying:

* “true fatigue labels”

Better wording:

* “PSD-defined fatigue states”
* “neural fatigue groups”
* “data-driven fatigue classes derived from PSD clustering”

That is more accurate and defensible.

---

## My strongest recommendation

For your setup, the best overall strategy is:

* **subject-wise GroupKFold**
* **K-means on PSD only within training folds**
* **binary, 3-class, 4-class analyzed separately**
* **30 s and 60 s compared explicitly**
* **Elastic Net multinomial classification**
* **stability-based feature ranking**
* **region-level first, channel-level second**
* **EOG vs EEG-ocular vs combined comparison**

This gives you both:

* clean validation
* interpretable best features

# Execution

use the conda environment `blinker_pyblinker_validation` which alredy dependecies installed.

# Experiment Output
All output should be saved in `D:\dataset\drowsy_driving_raja_processed\data\experimentation\exp1_blink_feature_fatigue_prediction\<hash>` where `<hash>` is a unique identifier for this experiment run, 

# Write a report
After running the experiment, write a report detailing about the experiment design, results, and interpretation in `writing/result/experiment2.tex`

# Skill
When developing the code, use the skill in agent_skillbook/skills to write modular, reusable code. 

For long experiment, it is compulsory to obey `agent_skillbook/skills/experiment-runbook-discipline` and save this in the `D:\dataset\drowsy_driving_raja_processed\data\experimentation\exp1_blink_feature_fatigue_prediction\<hash>` where `<hash>`