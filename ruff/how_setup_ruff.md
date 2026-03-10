
Run directly using Python:

```bash
py -m pipx install ruff
```

This always works even if PATH isn't refreshed.

---

## 🔥 After install — check + fix all issues

Inside your project:

```bash
ruff check .
```

Auto-fix:

```bash
ruff check . --fix
```

Format:

```bash
ruff check .
```


ruff check . --fix --unsafe-fixes

---
pip install --force-reinstall git+https://github.com/balandongiv/pyblinker.git@main