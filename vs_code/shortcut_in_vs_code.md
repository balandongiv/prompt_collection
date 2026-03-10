To wrap text in VS Code, you can use the following keyboard shortcut:
- On Windows/Linux: `Alt + Z`

To compile latex in VS Code, using the Xelatex engine, you can use the following steps:.
In the terminal

xelatex -shell-escape main.tex && xelatex -shell-escape main.tex


For Cleaning Up LaTeX Auxiliary Files:
```bash
latexmk -C
```

For extreme cleaning (removing all generated files including PDF):


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




