"""
Methodology Step 3: Literature Review Synthesizer.
Synthesizes Related Work narratives, generates comparative matrices,
and organizes BibTeX citation keys.
"""

from typing import Dict, Any, List
from modules.llm_provider import llm_service
import json
import re


def synthesize_literature_review(
    papers: List[Dict[str, Any]],
    proposed_work_title: str,
    research_gap: str,
    provider: str = "auto",
    model: str = None,
    api_key: str = None
) -> Dict[str, Any]:
    """
    Produces:
    1. A synthesized academic literature review narrative in Markdown/LaTeX citing the papers.
    2. A structured comparative analysis matrix.
    3. Aggregated BibTeX references.
    """
    papers_context = []
    bibtex_blocks = []
    matrix_rows = []

    for p in papers:
        title = p.get("title", "")
        authors = p.get("authors", [])
        first_author = authors[0].get("name", "Unknown") if authors and isinstance(authors[0], dict) else "Unknown"
        year = p.get("year", "2024")
        venue = p.get("venue", "arXiv")
        abstract = p.get("abstract", "")[:350]
        
        # Clean citation key
        from modules.semantic_scholar import clean_bibtex_key, paper_to_bibtex
        cite_key = clean_bibtex_key(first_author, year, title)
        p["citation_key"] = cite_key
        bibtex_blocks.append(paper_to_bibtex(p))

        papers_context.append(f"- \\cite{{{cite_key}}}: '{title}' by {first_author} et al. ({year}, {venue})\n  Summary: {abstract}")

        # Default matrix row
        matrix_rows.append({
            "author_year": f"{first_author} et al. ({year})",
            "method": title.split(":")[0][:30],
            "benchmark": venue,
            "pros": "Strong foundational performance and expressivity",
            "cons": "High computational complexity or scaling limitations",
            "citation_key": cite_key
        })

    prompt = f"""You are an elite academic researcher. Synthesize a publishable Related Work / Literature Review section for a scientific paper titled:
"{proposed_work_title}"

Identified Research Gap:
{research_gap}

Key Papers to Cite and Analyze:
{chr(10).join(papers_context) if papers_context else "Use classic foundational works: Vaswani et al. (2017) \\cite{vaswani2017attention}, Dao et al. (2022) \\cite{dao2022flashattention}, Gu et al. (2023) \\cite{gu2023mamba}."}

Requirements:
1. Divide into 2-3 logical thematic sub-headings (e.g. ### Dense Attention and Efficient Approximations, ### Structured State-Space Representations, ### Hardware-Aware Operator Fusion).
2. Use standard LaTeX citation commands e.g. \\cite{{key}}.
3. Contrast prior work critically with the proposed contribution.
4. Conclude with a clear positioning paragraph articulating how the proposed work resolves the limitations of the cited paradigms.
"""

    synthesis_narrative = llm_service.generate(
        prompt=prompt,
        system_prompt="You are an expert scientific writer. Write in formal, rigorous academic English.",
        provider=provider,
        model=model,
        api_key=api_key,
        task_context="lit_review"
    )

    return {
        "synthesis_text": synthesis_narrative,
        "matrix": matrix_rows,
        "bibtex_entries": "\n\n".join(bibtex_blocks)
    }
