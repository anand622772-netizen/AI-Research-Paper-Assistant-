@echo off
echo Compiling LaTeX Manuscript...
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
echo Compilation complete. Generated main.pdf
pause
