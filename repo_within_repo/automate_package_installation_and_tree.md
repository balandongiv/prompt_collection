# Worktree Setup Guide (Windows + Conda + VS Code)

This guide explains how to efficiently create and initialize a new Git worktree for `ear_eog_experiment` without manually pasting commands.

---

## ✅ Prerequisites

* Git installed

* Conda (Anaconda/Miniconda)

* Environment already created:

  ```
  blinker_pyblinker_validation
  ```

* Main repo path (adjust if different):

  ```
  C:\Users\balan\IdeaProjects\ear_eog_experiment
  ```

---

## 📁 Folder Structure (Recommended)

```
IdeaProjects/
│
├── ear_eog_experiment/        # main repo
├── shared/                   # optional shared deps (recommended)
│   ├── pyblinker/
│   ├── agent-skillbook/
│   └── mne-features/
```

---

## 🚀 One-Time Setup Scripts

Create a folder:

```
ear_eog_experiment\scripts\
```

---

### 1️⃣ `bootstrap-worktree.cmd`

```bat
@echo off
setlocal

set WORKTREE_DIR=%~1
if "%WORKTREE_DIR%"=="" (
    echo Missing worktree directory
    exit /b 1
)

cd /d "%WORKTREE_DIR%" || exit /b 1

echo Activating conda...
call C:\Users\balan\anaconda3\Scripts\activate.bat
call conda activate blinker_pyblinker_validation

echo Installing dependencies...

if not exist pyblinker (
    git clone --branch main https://github.com/balandongiv/pyblinker.git pyblinker
)
pip install -e .\pyblinker

if not exist agent_skillbook (
    git clone --branch main https://github.com/balandongiv/agent-skillbook.git agent_skillbook
)
pip install -e .\agent_skillbook

if not exist mne-features (
    git clone --branch master https://github.com/balandongiv/mne-features.git mne-features
)
pip install -e .\mne-features

echo.
echo ✅ Bootstrap complete.
```

---

### 2️⃣ `create-worktree.cmd`

```bat
@echo off
setlocal

set BRANCH_NAME=%~1
set WORKTREE_DIR=%~2
set MAIN_REPO=C:\Users\balan\IdeaProjects\ear_eog_experiment

if "%BRANCH_NAME%"=="" (
    echo Missing branch name
    exit /b 1
)

if "%WORKTREE_DIR%"=="" (
    echo Missing worktree directory
    exit /b 1
)

echo Creating worktree...
git -C "%MAIN_REPO%" worktree add "%WORKTREE_DIR%" -b "%BRANCH_NAME%" || exit /b 1

echo Running bootstrap...
call "%MAIN_REPO%\scripts\bootstrap-worktree.cmd" "%WORKTREE_DIR%"

echo.
echo ✅ Worktree ready at:
echo %WORKTREE_DIR%
```

---

## ▶️ Usage

From terminal:

```cmd
create-worktree.cmd feature_branch C:\Users\balan\IdeaProjects\ear_eog_experiment_feature_branch
```

---

## 💡 Optional (Recommended): Shared Dependencies

Instead of cloning dependencies in every worktree:

1. Clone once:

```cmd
git clone https://github.com/balandongiv/pyblinker.git C:\Users\balan\IdeaProjects\shared\pyblinker
git clone https://github.com/balandongiv/agent-skillbook.git C:\Users\balan\IdeaProjects\shared\agent-skillbook
git clone https://github.com/balandongiv/mne-features.git C:\Users\balan\IdeaProjects\shared\mne-features
```

2. Install from shared location:

```cmd
pip install -e C:\Users\balan\IdeaProjects\shared\pyblinker
pip install -e C:\Users\balan\IdeaProjects\shared\agent-skillbook
pip install -e C:\Users\balan\IdeaProjects\shared\mne-features
```

👉 Faster and avoids duplication across worktrees

---

## 🧪 Daily Workflow

### Create new worktree

```
create-worktree.cmd <branch> <folder>
```

### Re-run setup if needed

```
scripts\bootstrap-worktree.cmd <folder>
```

---

## ⚠️ Notes

* Prefer **Command Prompt (cmd)** instead of PowerShell 7 for Conda
* Ensure `conda init` has been run at least once
* Fix any typo like:

  ❌ `pip install -e .\agent_skillbookgit clone ...`
  ✅ split into two commands

---

## 🎯 Summary

* No more manual copy-paste
* One command = full environment ready
* Reproducible setup for every worktree

---
