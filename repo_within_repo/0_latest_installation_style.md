
What you want is:

* keep your main repo `BLINKER_PYBLINKER_VALIDATION`
* clone other repos like `pyblinker` and `ear_eog_experiment` as local folders
* install those repos in **editable mode**
* then when you change code inside those repos, your validation project immediately uses the updated code

Because you use **PowerShell** in VS Code, I’ll show the commands in PowerShell style.

---

# 1. First, understand the folder layout

You are working in:

```powershell
C:\Users\balan\IdeaProjects\blinker_pyblinker_validation
```

Inside that folder, you want local package folders such as:

```text
blinker_pyblinker_validation
├─ ear_eog_experiment
├─ pyblinker
├─ src
├─ tests
├─ reports
└─ ...
```

So `pyblinker` and `ear_eog_experiment` are inside the validation repo folder.

That is fine for local development.

One important note:
if `BLINKER_PYBLINKER_VALIDATION` is itself a git repo, then `pyblinker` and `ear_eog_experiment` are **nested git repos**. That is okay for local work, but usually you should add them to `.gitignore` in the outer repo so they are not accidentally tracked.

Example `.gitignore` entries:

```gitignore
pyblinker/
ear_eog_experiment/
```


---

# 3. Full step-by-step workflow in VS Code cmd

## Step 1: Open cmd in VS Code

You should see something like:

```powershell
PS C:\Users\balan\IdeaProjects\blinker_pyblinker_validation>
```

If conda is not initialized yet, do this once:

```powershell
C:\Users\balan\anaconda3\Scripts\activate
conda init powershell
```

Then restart the terminal.

---

## Step 2: In Idea, Activate your conda environment

```powershell
conda activate blinker_pyblinker_validation
```

Your prompt should become something like:

```powershell
(blinker_pyblinker_validation) PS C:\Users\balan\IdeaProjects\blinker_pyblinker_validation>
```


---

# 4. Clone `pyblinker` into the project folder

## Example: clone the `main` branch

```powershell
git clone --branch main https://github.com/balandongiv/pyblinker.git pyblinker
pip install -e .\pyblinker
```

This creates:

```text
C:\Users\balan\IdeaProjects\blinker_pyblinker_validation\pyblinker
```

## Install it in editable mode

From the validation repo root:

```powershell
pip install -e .\pyblinker
```

That means:

* Python imports `pyblinker` from that local folder
* if you edit code in `pyblinker`, your validation project sees it immediately

---

# 5. Clone `ear_eog_experiment` into the project folder

## Example: clone the `main` branch

```powershell
git clone --branch main https://github.com/balandongiv/ear_eog_experiment.git ear_eog_experiment
```

Then install it in editable mode:

```powershell
pip install -e .\ear_eog_experiment
```

Now your layout becomes:

```text
blinker_pyblinker_validation
├─ ear_eog_experiment
├─ pyblinker
├─ src
├─ tests
├─ reports
└─ ...
```
# Clone agent-skillbook if you want to work with it too
https://github.com/balandongiv/agent-skillbook

``` powershell
git clone --branch main https://github.com/balandongiv/agent-skillbook.git agent_skillbook
pip install -e .\agent_skillbook
```

# Clone mne-features
``` powershell
git clone --branch master https://github.com/balandongiv/mne-features.git mne-features

pip install -e .\mne-features
```
---

# 6. Verify that editable install worked

Run:

```powershell
pip list
```

or better:

```powershell
pip show pyblinker
pip show ear_eog_experiment
```

You should see their local install locations.

You can also run:

```powershell
python -c "import pyblinker; print(pyblinker.__file__)"
python -c "import ear_eog_experiment; print(ear_eog_experiment.__file__)"
```

That should point to the local folders inside your project.

---

# 7. Example: working with another branch instead of `main`

There are two common ways.

## Option A: clone directly from a specific branch

Example for branch `dev-feature-x`:

```powershell
git clone --branch dev-feature-x https://github.com/<your-user>/pyblinker.git pyblinker
pip install -e .\pyblinker
```

Same for `ear_eog_experiment`:

```powershell
git clone --branch experiment-branch https://github.com/balandongiv/ear_eog_experiment.git ear_eog_experiment
pip install -e .\ear_eog_experiment
```

---

## Option B: clone once, then switch branch later

This is usually better.

Clone once:

```powershell
git clone https://github.com/<your-user>/pyblinker.git pyblinker
pip install -e .\pyblinker
```

Then later, switch branch:

```powershell
cd .\pyblinker
git fetch --all
git switch main
```

or:

```powershell
git switch dev-feature-x
```

Then go back:

```powershell
cd ..
```

Because it is already installed in editable mode, you usually do **not** need to reinstall after branch switch, unless dependencies changed.

If dependencies changed, run again:

```powershell
pip install -e .\pyblinker
```

---

# 8. Do you need to delete `pyblinker` to use another branch?

Usually **no**.

The more efficient way is:

```powershell
cd .\pyblinker
git fetch --all
git switch other-branch
cd ..
```

That is much better than deleting and recloning.

---

# 9. If you really want to delete `pyblinker`

From the project root:

```powershell
Remove-Item -Recurse -Force .\pyblinker
```

Then clone again:

```powershell
git clone --branch other-branch https://github.com/<your-user>/pyblinker.git pyblinker
pip install -e .\pyblinker
```

---

# 10. Better alternatives than deleting folders

There are three better approaches.

## Method 1: switch branches in the same folder

Best when you only need one branch at a time.

```powershell
cd .\pyblinker
git fetch --all
git switch main
# or
git switch feature-branch
cd ..
```

## Method 2: use `git worktree`

Best when you want multiple branches checked out at the same time.

Example:

```powershell
cd .\pyblinker
git worktree add ..\pyblinker_feature_x feature-x
```

Now you have:

```text
blinker_pyblinker_validation
├─ pyblinker
├─ pyblinker_feature_x
├─ ear_eog_experiment
├─ src
├─ tests
└─ ...
```

Then install whichever one you want:

```powershell
pip install -e .\pyblinker_feature_x
```

This is very efficient because you do not reclone the repo.

## Method 3: keep separate clones per branch

Simple but uses more disk space.

Example:

```powershell
git clone --branch main https://github.com/<your-user>/pyblinker.git pyblinker_main
git clone --branch feature-x https://github.com/<your-user>/pyblinker.git pyblinker_feature_x
```

Then install the one you want:

```powershell
pip install -e .\pyblinker_main
```

or

```powershell
pip install -e .\pyblinker_feature_x
```

---

# 11. Recommended practical workflow

For your case, I recommend this:

## First time only

```powershell
conda init powershell
```

Restart terminal.

## Every new VS Code session

```powershell
conda activate blinker_pyblinker_validation
cd C:\Users\balan\IdeaProjects\blinker_pyblinker_validation
```

## Clone packages once

```powershell
git clone https://github.com/<your-user>/pyblinker.git pyblinker
git clone https://github.com/balandongiv/ear_eog_experiment.git ear_eog_experiment
```

## Install editable

```powershell
pip install -e .\pyblinker
pip install -e .\ear_eog_experiment
```

## Switch package branch when needed

```powershell
cd .\pyblinker
git fetch --all
git switch feature-branch
cd ..
```

If branch adds dependencies:

```powershell
pip install -e .\pyblinker
```

---

# 12. Complete example from start to finish

Here is a full session in PowerShell.

## A. Start terminal and activate env

```powershell
conda activate blinker_pyblinker_validation
cd C:\Users\balan\IdeaProjects\blinker_pyblinker_validation
```

## B. Clone `pyblinker` main

```powershell
git clone --branch main https://github.com/<your-user>/pyblinker.git pyblinker
pip install -e .\pyblinker
```

## C. Clone `ear_eog_experiment` main

```powershell
git clone --branch main https://github.com/balandongiv/ear_eog_experiment.git ear_eog_experiment
pip install -e .\ear_eog_experiment
```

## D. Later, switch `pyblinker` to another branch

```powershell
cd .\pyblinker
git fetch --all
git switch my-feature-branch
cd ..
pip install -e .\pyblinker
```

---
# agent skillbook

```powershell`
git clone --branch main  https://github.com/balandongiv/agent-skillbook.git agent-skillbook

pip install -e .\agent-skillbook
```
```powershell
# 13. If you get “folder already exists”

If you try to clone into `pyblinker` but it already exists, Git will fail.

Check first:

```powershell
Get-ChildItem
```

If `pyblinker` already exists, either:

## switch branch inside it

```powershell
cd .\pyblinker
git branch
git switch main
cd ..
```

or delete it:

```powershell
Remove-Item -Recurse -Force .\pyblinker
```

and clone again.

---

# 14. One small correction about “sibling folder”

You wrote:

> From inside BLINKER_PYBLINKER_VALIDATION, clone it as a sibling folder

Technically, if you clone while standing inside `blinker_pyblinker_validation`, then `pyblinker` and `ear_eog_experiment` become:

* sibling folders to `src`, `tests`, `reports`
* but **child folders** of `blinker_pyblinker_validation`

So the path is:

```text
C:\Users\balan\IdeaProjects\blinker_pyblinker_validation\pyblinker
C:\Users\balan\IdeaProjects\blinker_pyblinker_validation\ear_eog_experiment
```

That matches your intended layout.

---

# 15. Best answer to your main question

For your workflow, the most efficient approach is:

* clone each package once
* install with `pip install -e`
* switch branches with `git switch`
* only reinstall with `pip install -e` when dependencies or packaging metadata changed
* do **not** delete and re-clone unless the folder is broken or you want a completely fresh copy

And for PowerShell, use:

```powershell
conda init powershell
```

not:

```powershell
conda init cmd.exe
```

---

Here is the shortest practical command set for your case:

```powershell
conda activate blinker_pyblinker_validation
cd C:\Users\balan\IdeaProjects\blinker_pyblinker_validation

git clone --branch main https://github.com/<your-user>/pyblinker.git pyblinker
git clone --branch main https://github.com/balandongiv/ear_eog_experiment.git ear_eog_experiment
git clone --branch master https://github.com/mne-tools/mne-features.git mne_features
pip install -e .\pyblinker
pip install -e .\ear_eog_experiment


pip install -e .\mne_features

```

Then later:

```powershell
cd .\pyblinker
git fetch --all
git switch another-branch
cd ..
pip install -e .\pyblinker
```

I can also turn this into a clean `README` section or a reusable PowerShell script for your repo.
