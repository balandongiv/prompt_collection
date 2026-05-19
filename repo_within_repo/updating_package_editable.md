Since you installed it in editable mode, updating is usually just a Git pull in the cloned repo.

If you originally did:

```bash
git clone --branch main https://github.com/balandongiv/pyblinker.git pyblinker
pip install -e .\pyblinker
```

then later you can update it like this:

```bash
cd pyblinker
git pull
```

That is often enough, because `pip install -e` points Python to your local source folder, so when the source changes, your environment uses the updated code right away.

If the package dependencies or metadata changed, run the editable install again:

```bash
pip install -e .
```

A safe full update flow is:

```bash
cd pyblinker
git pull
pip install -e .
```

If you want to make sure you are on `main` first:

```bash
cd pyblinker
git checkout main
git pull origin main
pip install -e .
```

A few useful checks:

```bash
git status
git branch
pip show pyblinker
```

If `git pull` complains because you changed local files, either commit them, stash them, or discard them before pulling.

For Windows PowerShell, your original style is fine. After cloning, updates are done inside the repo folder, not by cloning again.
