Use this inside your VS Code devcontainer terminal.

### 1. Create the environment

```bash
cd /workspaces/ear_eog_experiment_enhance_experiment_flow
python -m venv eog_ear_experiment
```

### 2. Activate it now

```bash
source /workspaces/ear_eog_experiment_enhance_experiment_flow/eog_ear_experiment/bin/activate
```

You should see:

```bash
(eog_ear_experiment) vscode ➜ /workspaces/ear_eog_experiment_enhance_experiment_flow $
```

### 3. Make every new terminal activate it automatically

Add this to `~/.bashrc`:

```bash
cat >> ~/.bashrc <<'EOF'

# Auto-activate project venv
if [ -f /workspaces/ear_eog_experiment_enhance_experiment_flow/eog_ear_experiment/bin/activate ]; then
  source /workspaces/ear_eog_experiment_enhance_experiment_flow/eog_ear_experiment/bin/activate
fi
EOF
```

### 4. Reload bash config

```bash
source ~/.bashrc
```

### 5. Test it

Close the current terminal in VS Code, then open a new terminal.

It should automatically show:

```bash
(eog_ear_experiment) vscode ➜ /workspaces/ear_eog_experiment_enhance_experiment_flow $
```

### Optional: also select it in VS Code Python

Run:

* `Ctrl+Shift+P`
* `Python: Select Interpreter`
* choose
  `/workspaces/ear_eog_experiment_enhance_experiment_flow/eog_ear_experiment/bin/python`

### One-shot version

If you want to do it all at once:

```bash
cd /workspaces/ear_eog_experiment_enhance_experiment_flow
python -m venv eog_ear_experiment
source eog_ear_experiment/bin/activate

cat >> ~/.bashrc <<'EOF'

# Auto-activate project venv
if [ -f /workspaces/ear_eog_experiment_enhance_experiment_flow/eog_ear_experiment/bin/activate ]; then
  source /workspaces/ear_eog_experiment_enhance_experiment_flow/eog_ear_experiment/bin/activate
fi
EOF

source ~/.bashrc
```

If you want this baked into your devcontainer so it always works after rebuilds, add the same activation block into `post-start.sh`.



I’m editing three things together: the devcontainer mount list, the worktree .git pointer, and the utilities section of the flowchart so the repair is documented as part of the repo’s execution
contract. After that I’ll do a static verification pass and call out the one remaining step you need to apply it: rebuild/reopen the container so the new mount exists.

Next step:

1. In VS Code, run Dev Containers: Rebuild Container or Reopen in Container.
2. After rebuild, check:
```bash
ls /workspaces/.git-admin/ear_eog_experiment.git
git rev-parse --show-toplevel
git status
```