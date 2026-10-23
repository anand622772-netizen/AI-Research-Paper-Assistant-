"""
LaTeX Compilation & Packaging Engine.
Handles ZIP package export for Overleaf, local compilation checks,
and build scripts.
"""

import os
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


def check_local_latex_compilers() -> Dict[str, bool]:
    """Checks whether local LaTeX compilers are available in PATH."""
    compilers = ["pdflatex", "xelatex", "lualatex", "latexmk", "tectonic"]
    status = {}
    for comp in compilers:
        status[comp] = shutil.which(comp) is not None
    return status


def create_latex_package(
    output_dir: Path,
    main_tex: str,
    bibtex_content: str,
    figures_list: List[Dict[str, Any]],
    project_name: str = "research_paper"
) -> Tuple[Path, Path]:
    """
    Creates a complete compile-ready LaTeX directory and a downloadable ZIP archive.
    Returns (package_dir, zip_filepath).
    """
    clean_name = "".join(c for c in project_name if c.isalnum() or c in ("_", "-")).strip() or "paper"
    pkg_dir = output_dir / clean_name
    pkg_dir.mkdir(parents=True, exist_ok=True)
    
    figures_dir = pkg_dir / "figures"
    figures_dir.mkdir(exist_ok=True)

    # 1. Write main.tex
    with open(pkg_dir / "main.tex", "w", encoding="utf-8") as f:
        f.write(main_tex)

    # 2. Write references.bib
    with open(pkg_dir / "references.bib", "w", encoding="utf-8") as f:
        f.write(bibtex_content)

    # 3. Copy figures
    for fig in figures_list:
        fname = fig.get("filename", "")
        # Check in outputs or parent outputs
        possible_paths = [
            output_dir / fname,
            output_dir / "plots" / fname,
            Path(fig.get("path", ""))
        ]
        for p in possible_paths:
            if p.exists() and p.is_file():
                shutil.copy2(p, pkg_dir / p.name)
                shutil.copy2(p, figures_dir / p.name)
                break

    # 4. Windows compile.bat
    compile_bat = """@echo off
echo Compiling LaTeX Manuscript...
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
echo Compilation complete. Generated main.pdf
pause
"""
    with open(pkg_dir / "compile.bat", "w", encoding="utf-8") as f:
        f.write(compile_bat)

    # 5. Linux/macOS Makefile
    makefile = """all:
\tpdflatex -interaction=nonstopmode main.tex
\tbibtex main
\tpdflatex -interaction=nonstopmode main.tex
\tpdflatex -interaction=nonstopmode main.tex

clean:
\trm -f *.aux *.bbl *.blg *.log *.out *.toc *.synctex.gz
"""
    with open(pkg_dir / "Makefile", "w", encoding="utf-8") as f:
        f.write(makefile)

    # 6. Overleaf instructions README
    readme = """AI Research Paper Assistant - LaTeX Manuscript Package
======================================================
1. To compile on Overleaf:
   - Create a 'New Project' -> 'Upload Project'
   - Upload this entire ZIP archive
   - Select 'main.tex' as the root file
   - Click 'Recompile'

2. To compile locally:
   - Windows: double-click 'compile.bat'
   - Linux/Mac: type 'make' in your terminal
"""
    with open(pkg_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme)

    # 7. Create ZIP archive
    zip_path = output_dir / f"{clean_name}_latex_bundle.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(pkg_dir):
            for file in files:
                abs_f = Path(root) / file
                rel_f = abs_f.relative_to(pkg_dir)
                zf.write(abs_f, arcname=str(rel_f))

    return pkg_dir, zip_path


def attempt_local_compile(pkg_dir: Path) -> Tuple[bool, Optional[Path], str]:
    """
    Attempts to compile main.tex locally using pdflatex or tectonic if available.
    Returns (success, pdf_path, log_output).
    """
    compilers = check_local_latex_compilers()
    main_tex = pkg_dir / "main.tex"
    pdf_out = pkg_dir / "main.pdf"

    if compilers.get("tectonic"):
        cmd = ["tectonic", str(main_tex)]
    elif compilers.get("pdflatex"):
        cmd = ["pdflatex", "-interaction=nonstopmode", "main.tex"]
    else:
        return False, None, "No local LaTeX compiler (pdflatex, tectonic) was found in system PATH. You can download the ZIP package and compile it directly on Overleaf or local TeX Live/MiKTeX."

    try:
        res = subprocess.run(cmd, cwd=pkg_dir, capture_output=True, text=True, timeout=30)
        if pdf_out.exists():
            return True, pdf_out, res.stdout
        return False, None, f"Compiler exited with code {res.returncode}.\n{res.stdout}\n{res.stderr}"
    except Exception as e:
        return False, None, str(e)
