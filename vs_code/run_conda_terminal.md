Use this one-liner in Windows terminal:

```bat
conda run -n pyblinker python -m blinker_pyblinker_validation.blink_compare
```

That runs the command inside the `pyblinker` conda env **without needing activation first**.

If `conda` itself is not found, use the full Conda hook form for `cmd`:

```bat
CALL conda.bat activate pyblinker && python -m blinker_pyblinker_validation.blink_compare
```

If you're in PowerShell:

```powershell
conda run -n pyblinker python -m blinker_pyblinker_validation.blink_compare
```

Best choice for agents/scripts is usually:

```bat
conda run -n pyblinker python -m blinker_pyblinker_validation.blink_compare
```

because it is more reliable than assuming the shell already activated the env.
