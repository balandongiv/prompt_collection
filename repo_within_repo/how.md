Yep — if you are already here:

```bash
(pyblinker) C:\Users\balan\IdeaProjects\pyblinker\pyblinker>
```

then you do **not** need `cd` again.

Use these commands directly.

## Install the repo under the current folder

Clone it into the current `pyblinker` folder:

```bash
git clone https://github.com/balandongiv/blinker_pyblinker_validation.git
```

Install it in editable mode:

```bash
python -m pip install -e .\blinker_pyblinker_validation
```

## How to work on it

Edit files inside:

```text
.\blinker_pyblinker_validation\
```

Then commit and push from inside that repo:

```bash
cd .\blinker_pyblinker_validation
git status
git add .
git commit -m "your message"
git push origin main
```

Then return to your main repo if needed:

```bash
cd ..
```

## How to uninstall

To uninstall the package from your virtual environment:

```bash
python -m pip uninstall blinker_pyblinker_validation
```

If that package name does not match exactly, first check the installed name:

```bash
python -m pip list
```

or:

```bash
python -m pip show blinker_pyblinker_validation
```

Sometimes the install name differs slightly from the folder name. If uninstall says it cannot find it, use the package name shown by `pip list`.

## If you want to remove it completely

Uninstall the Python package:

```bash
python -m pip uninstall blinker_pyblinker_validation
```

Then delete the cloned repo folder:

```bash
rmdir /s /q blinker_pyblinker_validation
```

## Full command sequence from your current prompt

```bash
git clone https://github.com/balandongiv/blinker_pyblinker_validation.git
python -m pip install -e .\blinker_pyblinker_validation
```

Later, uninstall:

```bash
python -m pip uninstall blinker_pyblinker_validation
```

And optionally delete the folder:

```bash
rmdir /s /q blinker_pyblinker_validation
```

One small caution: if `blinker_pyblinker_validation` is inside your main repo folder, your outer `pyblinker` git may show it as an untracked nested repo. If you do not want that, add this to the outer `.gitignore`:

```gitignore
blinker_pyblinker_validation/
```
