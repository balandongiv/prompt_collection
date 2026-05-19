blinker_fatigue_experiment


Yes — for your case, the best way is to create the environment with **Conda first**, and only fall back to `pip` for anything Conda cannot provide.

The good news is that **all the packages you listed appear to be available on conda-forge**, including `mne-features`, `autoreject`, `mne`, and `llvmlite`. ([Anaconda][1])

Use this command:

```bat
conda create -n blinker_fatigue_experiment -c conda-forge python=3.11 tqdm pyyaml jinja2 gdown pyarrow defusedxml mne mne-features autoreject seaborn pandas scikit-learn llvmlite numpy scipy matplotlib -y
```

Then activate it:

```bat
conda activate blinker_fatigue_experiment
```

Why this helps on Windows:

* Conda installs prebuilt binaries for packages like `numpy`, `scipy`, and `llvmlite`, which is often more stable on Windows than mixing pip wheels with BLAS-linked scientific packages. ([Anaconda][2])
* Installing from **conda-forge** in one shot reduces ABI and BLAS mismatch problems.

I also added:

* `python=3.11`
* `numpy`
* `scipy`
* `matplotlib`

Those are not all listed in your file, but they are common dependencies in this stack and keeping them Conda-managed usually makes the environment more stable on Windows.

After installation, verify:

```bat
conda list
python -c "import numpy, scipy, pandas, sklearn, mne, mne_features, autoreject; print('OK')"
```

If you want an `environment.yml`, use this:

```yaml
name: blinker_fatigue_experiment
channels:
  - conda-forge
dependencies:
  - python=3.11
  - numpy
  - scipy
  - matplotlib
  - pandas
  - scikit-learn
  - seaborn
  - tqdm
  - pyyaml
  - jinja2
  - gdown
  - pyarrow
  - defusedxml
  - mne
  - mne-features
  - autoreject
  - llvmlite
```

Create it with:

```bat
conda env create -f environment.yml
conda activate blinker_fatigue_experiment
```

One important note: your original lines

```txt
mne-features @ https://github.com/mne-tools/mne-features.git#egg=mne_features
autoreject @ https://github.com/autoreject/autoreject/archive/refs/heads/main.zip
```

are **pip-style direct URL installs**. For this environment, do **not** use those URLs unless you specifically need the latest GitHub code. Prefer the Conda packages instead, since they are available and are less likely to trigger the Windows BLAS/Numpy problems you want to avoid. ([Anaconda][1])

If Conda still shows the duplicate env-path issue afterward, it won’t affect this new environment’s functionality; it is usually just duplicate registration of the same path in `environments.txt`.

[1]: https://anaconda.org/conda-forge/mne-features?utm_source=chatgpt.com "mne-features - conda-forge"
[2]: https://anaconda.org/conda-forge/llvmlite/?utm_source=chatgpt.com "llvmlite - conda-forge"
