"""
LaTeX Templates repository for AI Research Paper Assistant.
Provides formal conference styles: NeurIPS, IEEEtran, ACM SIGCONF, Nature, and Standard Article.
"""

from typing import Dict, Any, List
import re


def markdown_to_latex(text: str) -> str:
    """
    Converts markdown headers, bold, italics, and lists into LaTeX commands
    while preserving native LaTeX math and environments.
    """
    lines = text.split("\n")
    tex_lines = []
    in_itemize = False
    in_enumerate = False

    for line in lines:
        stripped = line.strip()

        # Check list closures
        if not (stripped.startswith("- ") or stripped.startswith("* ")) and in_itemize:
            tex_lines.append("\\end{itemize}")
            in_itemize = False
        if not re.match(r"^\d+\.\s+", stripped) and in_enumerate:
            tex_lines.append("\\end{enumerate}")
            in_enumerate = False

        # Section headers
        if stripped.startswith("### "):
            header = stripped[4:].strip()
            tex_lines.append(f"\\subsubsection{{{header}}}")
        elif stripped.startswith("## "):
            header = stripped[3:].strip()
            tex_lines.append(f"\\subsection{{{header}}}")
        elif stripped.startswith("# "):
            header = stripped[2:].strip()
            tex_lines.append(f"\\section{{{header}}}")

        # Unordered list items
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_itemize:
                tex_lines.append("\\begin{itemize}")
                in_itemize = True
            item_text = stripped[2:].strip()
            tex_lines.append(f"  \\item {item_text}")

        # Ordered list items
        elif re.match(r"^\d+\.\s+", stripped):
            if not in_enumerate:
                tex_lines.append("\\begin{enumerate}")
                in_enumerate = True
            item_text = re.sub(r"^\d+\.\s+", "", stripped)
            tex_lines.append(f"  \\item {item_text}")

        else:
            tex_lines.append(line)

    if in_itemize:
        tex_lines.append("\\end{itemize}")
    if in_enumerate:
        tex_lines.append("\\end{enumerate}")

    converted = "\n".join(tex_lines)

    # Convert bold **text** to \textbf{text}
    converted = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", converted)
    # Convert italic *text* to \textit{text}
    converted = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\textit{\1}", converted)

    return converted


def render_latex_manuscript(
    template_name: str,
    metadata: Dict[str, Any],
    abstract: str,
    sections: Dict[str, str],
    custom_preamble: str = ""
) -> str:
    """
    Assembles a complete, compilation-ready LaTeX document (.tex).
    """
    title = metadata.get("title", "Manuscript Title")
    authors = metadata.get("authors", [{"name": "Author Name", "affiliation": "Institution", "email": "author@domain.edu"}])
    keywords = metadata.get("keywords", ["Artificial Intelligence", "Deep Learning"])
    kw_str = ", ".join(keywords)

    # Build author blocks
    author_tex = ""
    if "IEEE" in template_name:
        author_blocks = []
        for a in authors:
            author_blocks.append(f"\\IEEEauthorblockN{{{a.get('name')}}}\n\\IEEEauthorblockA{{{a.get('affiliation')}}}\\\\Email: \\texttt{{{a.get('email')}}}")
        author_tex = " \\and\n".join(author_blocks)
        author_tex = f"\\author{{\n{author_tex}\n}}"
    elif "ACM" in template_name:
        author_blocks = []
        for a in authors:
            author_blocks.append(f"\\author{{{a.get('name')}}}\n\\affiliation{{\\institution{{{a.get('affiliation')}}}}}\n\\email{{{a.get('email')}}}")
        author_tex = "\n".join(author_blocks)
    else:
        author_names = " \\and ".join([f"{a.get('name')}\\\\ \\small {a.get('affiliation')}" for a in authors])
        author_tex = f"\\author{{{author_names}}}"

    # Assemble section bodies
    sections_tex = []
    for sec_title, sec_content in sections.items():
        if sec_title.lower() == "abstract":
            continue
        clean_title = re.sub(r"^\d+\.\s*", "", sec_title)
        conv_body = markdown_to_latex(sec_content)
        sections_tex.append(f"\\section{{{clean_title}}}\n{conv_body}\n")

    full_body_tex = "\n\n".join(sections_tex)

    if "IEEE" in template_name:
        return f"""\\documentclass[conference]{{IEEEtran}}
\\IEEEoverridecommandlockouts
\\usepackage{{cite}}
\\usepackage{{amsmath,amssymb,amsfonts}}
\\usepackage{{algorithmic}}
\\usepackage{{graphicx}}
\\usepackage{{textcomp}}
\\usepackage{{xcolor}}
\\usepackage{{booktabs}}
\\usepackage{{hyperref}}
{custom_preamble}

\\begin{{document}}

\\title{{{title}}}

{author_tex}

\\maketitle

\\begin{{abstract}}
{abstract}
\\end{{abstract}}

\\begin{{IEEEkeywords}}
{kw_str}
\\end{{IEEEkeywords}}

{full_body_tex}

\\bibliographystyle{{IEEEtran}}
\\bibliography{{references}}

\\end{{document}}
"""

    elif "ACM" in template_name:
        return f"""\\documentclass[sigconf]{{acmart}}
\\usepackage{{booktabs}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}
{custom_preamble}

\\begin{{document}}

\\title{{{title}}}

{author_tex}

\\begin{{abstract}}
{abstract}
\\end{{abstract}}

\\keywords{{{kw_str}}}

\\maketitle

{full_body_tex}

\\bibliographystyle{{ACM-Reference-Format}}
\\bibliography{{references}}

\\end{{document}}
"""

    elif "NeurIPS" in template_name:
        return f"""\\documentclass{{article}}
\\usepackage[preprint]{{neurips_2024}} % neurips preprint style
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{hyperref}}
\\usepackage{{url}}
\\usepackage{{booktabs}}
\\usepackage{{amsfonts}}
\\usepackage{{amsmath}}
\\usepackage{{nicefrac}}
\\usepackage{{microtype}}
\\usepackage{{graphicx}}
{custom_preamble}

\\title{{{title}}}

{author_tex}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
{abstract}
\\end{{abstract}}

{full_body_tex}

\\bibliographystyle{{plain}}
\\bibliography{{references}}

\\end{{document}}
"""

    else:
        # Standard Universal Academic Article
        return f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{amsmath,amssymb,amsfonts,amsthm}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{microtype}}
\\usepackage{{hyperref}}
\\hypersetup{{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}}
{custom_preamble}

\\title{{\\textbf{{{title}}}}}
{author_tex}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
{abstract}
\\vspace{{0.5em}}

\\noindent\\textbf{{Keywords:}} {kw_str}
\\end{{abstract}}

{full_body_tex}

\\bibliographystyle{{abbrv}}
\\bibliography{{references}}

\\end{{document}}
"""
