Use this complete command from your project root to delete common LaTeX auxiliary files in **all folders and subfolders**:

```bash
find . -type f \( \
-name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o \
-name "*.lof" -o -name "*.lot" -o -name "*.fls" -o -name "*.fdb_latexmk" -o \
-name "*.synctex.gz" -o -name "*.bbl" -o -name "*.blg" -o -name "*.bcf" -o \
-name "*.run.xml" -o -name "*.nav" -o -name "*.snm" -o -name "*.vrb" -o \
-name "*.xdv" -o -name "*.dvi" -o -name "*.ps" -o -name "*.idx" -o \
-name "*.ilg" -o -name "*.ind" -o -name "*.acn" -o -name "*.acr" -o \
-name "*.alg" -o -name "*.glg" -o -name "*.glo" -o -name "*.gls" -o \
-name "*.ist" -o -name "*.xdy" \
\) -print -delete
```

Preview first without deleting:

```bash
find . -type f \( \
-name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o \
-name "*.lof" -o -name "*.lot" -o -name "*.fls" -o -name "*.fdb_latexmk" -o \
-name "*.synctex.gz" -o -name "*.bbl" -o -name "*.blg" -o -name "*.bcf" -o \
-name "*.run.xml" -o -name "*.nav" -o -name "*.snm" -o -name "*.vrb" -o \
-name "*.xdv" -o -name "*.dvi" -o -name "*.ps" -o -name "*.idx" -o \
-name "*.ilg" -o -name "*.ind" -o -name "*.acn" -o -name "*.acr" -o \
-name "*.alg" -o -name "*.glg" -o -name "*.glo" -o -name "*.gls" -o \
-name "*.ist" -o -name "*.xdy" \
\) -print
```

If you also want to remove the generated PDF:

```bash
find . -type f \( \
-name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o \
-name "*.lof" -o -name "*.lot" -o -name "*.fls" -o -name "*.fdb_latexmk" -o \
-name "*.synctex.gz" -o -name "*.bbl" -o -name "*.blg" -o -name "*.bcf" -o \
-name "*.run.xml" -o -name "*.nav" -o -name "*.snm" -o -name "*.vrb" -o \
-name "*.xdv" -o -name "*.dvi" -o -name "*.ps" -o -name "*.idx" -o \
-name "*.ilg" -o -name "*.ind" -o -name "*.acn" -o -name "*.acr" -o \
-name "*.alg" -o -name "*.glg" -o -name "*.glo" -o -name "*.gls" -o \
-name "*.ist" -o -name "*.xdy" -o -name "*.pdf" \
\) -print -delete
```

A shorter option, if you use `latexmk`, is:

```bash
latexmk -C
```

That usually removes most generated LaTeX files.

xelatex -shell-escape main.tex && xelatex -shell-escape main.tex
