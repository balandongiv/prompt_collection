# Fixing Dev Container Shell Script Line Endings on Windows

## Overview

This tutorial shows how to diagnose and fix a Dev Container startup failure caused by **Windows CRLF line endings** in shell scripts.

This issue commonly appears when:

* you develop on Windows,
* your Dev Container runs Linux,
* and `.sh` files are saved with `CRLF` instead of `LF`.

---

## 1. Symptom

The Dev Container starts, but VS Code fails when running the setup script from `devcontainer.json`.

Typical log output looks like this:

```text
Running the onCreateCommand from devcontainer.json...
Start: Run in container: /bin/sh -c bash .devcontainer/scripts/on-create.sh
: invalid option name/on-create.sh: line 2: set: pipefail
onCreateCommand from devcontainer.json failed with exit code 2.
Skipping any further user-provided commands.
```

### What this means

Your script contains a line like:

```bash
set -euo pipefail
```

That line is valid in Bash.
So if Bash says `pipefail` is invalid, the usual cause is that the script was saved with **CRLF** line endings, and Bash is actually reading:

```bash
pipefail\r
```

That hidden `\r` breaks the command.

---

## 2. Root Cause

The script file on disk was saved with **CRLF** line endings.

In a Linux container, shell scripts should use **LF** line endings.

A check with Git usually confirms it:

```bash
git ls-files --eol .devcontainer/scripts/on-create.sh
```

Bad result:

```text
i/lf    w/crlf  attr/text eol=lf        .devcontainer/scripts/on-create.sh
```

### Meaning

* `i/lf` = Git index stores the file as LF
* `w/crlf` = working copy on disk is CRLF
* `attr/text eol=lf` = `.gitattributes` says the file should be LF

So Git knows the file should be LF, but the actual file on disk is still CRLF.

---

## 3. The Fix

### Step 1: Add `.gitattributes`

Create a file named `.gitattributes` in the project root.

Recommended rule:

```gitattributes
*.sh text eol=lf
```

Or, if you want to target only Dev Container scripts:

```gitattributes
.devcontainer/scripts/*.sh text eol=lf
```

---

### Step 2: Convert the affected script to LF

Open the broken file in VS Code:

```text
.devcontainer/scripts/on-create.sh
```

Then:

1. Look at the bottom-right corner of VS Code
2. Click `CRLF`
3. Change it to `LF`
4. Save the file

If needed, do the same for:

```text
.devcontainer/scripts/post-start.sh
```

---

### Step 3: Verify the line endings

Run:

```bash
git ls-files --eol .devcontainer/scripts/on-create.sh
git ls-files --eol .devcontainer/scripts/post-start.sh
```

Correct result:

```text
i/lf    w/lf    attr/text eol=lf        .devcontainer/scripts/on-create.sh
i/lf    w/lf    attr/text eol=lf        .devcontainer/scripts/post-start.sh
```

This means both the Git index and the working copy are now using LF.

---

## 4. The Commit

Stage and commit the fix:

```bash
git add .gitattributes .devcontainer/scripts/on-create.sh .devcontainer/scripts/post-start.sh
git commit -m "Fix devcontainer shell script line endings"
```

A good alternative commit message is:

```text
Normalize shell scripts to LF for devcontainer
```

---

## 5. Rebuild the Dev Container

After committing, rebuild the container in VS Code:

1. Open Command Palette
2. Run:

```text
Dev Containers: Rebuild Container
```

This forces the container to rerun the setup using the corrected scripts.

---

## 6. Final Checks

Use this checklist to confirm everything is fixed.

### File checks

Run:

```bash
git ls-files --eol .devcontainer/scripts/on-create.sh
git ls-files --eol .devcontainer/scripts/post-start.sh
```

Expected:

```text
w/lf
```

for both files.

---

### Git attributes check

Make sure `.gitattributes` exists in the repo root and contains:

```gitattributes
*.sh text eol=lf
```

---

### Container startup check

Rebuild the container and confirm that:

* `onCreateCommand` runs successfully
* `postStartCommand` is no longer skipped
* there is no `set: pipefail` error
* there is no `invalid option name` error

---

### Success indicator

A successful fix means:

* the Dev Container opens normally,
* setup scripts run,
* no shell parsing error appears,
* no line-ending mismatch remains.

---

## 7. Quick Summary

### Symptom

Dev Container fails during `onCreateCommand` with a Bash error like:

```text
set: pipefail: invalid option name
```

### Cause

Shell script saved with **CRLF** instead of **LF**.

### Fix

* add `.gitattributes`
* enforce `*.sh text eol=lf`
* convert affected `.sh` files to LF
* rebuild the container

### Commit

```bash
git commit -m "Fix devcontainer shell script line endings"
```

### Verification

```bash
git ls-files --eol .devcontainer/scripts/on-create.sh
git ls-files --eol .devcontainer/scripts/post-start.sh
```

Expected:

```text
i/lf    w/lf    attr/text eol=lf
```

---

