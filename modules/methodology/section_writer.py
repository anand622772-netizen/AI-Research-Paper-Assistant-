"""
Methodology Step 4: Section Writing Studio.
Generates and refines individual paper sections with academic rigor,
mathematical equations, algorithmic pseudo-code, and tables.
"""

from typing import Dict, Any, List, Optional
from modules.llm_provider import llm_service


def draft_paper_section(
    section_name: str,
    paper_metadata: Dict[str, Any],
    outline_item: Optional[Dict[str, Any]],
    research_insights: Dict[str, Any],
    cited_papers: List[Dict[str, Any]],
    tone: str = "Formal Academic (Top-tier Conference)",
    include_equations: bool = True,
    include_algorithms: bool = False,
    include_tables: bool = False,
    provider: str = "auto",
    model: str = None,
    api_key: str = None
) -> str:
    """
    Drafts a complete, context-aware section for the academic manuscript.
    """
    title = paper_metadata.get("title", "Research Manuscript")
    target_words = outline_item.get("target_words", 800) if outline_item else 800
    objective = outline_item.get("objective", f"Elaborate on {section_name}") if outline_item else ""
    bullets = outline_item.get("bullet_points", []) if outline_item else []

    papers_keys = []
    for p in cited_papers[:5]:
        authors = p.get("authors", [])
        fa = authors[0].get("name", "Unknown") if authors and isinstance(authors[0], dict) else "Unknown"
        papers_keys.append(f"\\cite{{{p.get('citation_key', 'author2024')}}} ({fa} et al.)")

    formatting_rules = []
    if include_equations:
        formatting_rules.append("- Include standard numbered LaTeX equation blocks using \\begin{equation} ... \\end{equation} or \\begin{align} ... \\end{align} with formal mathematical definitions.")
    if include_algorithms:
        formatting_rules.append("- Include a LaTeX algorithmic pseudocode block (using \\begin{algorithmic} or clear algorithmic notation) detailing the key procedure.")
    if include_tables:
        formatting_rules.append("- Include a publication-grade LaTeX table with \\begin{table}[htbp], \\centering, \\toprule, \\midrule, \\bottomrule from booktabs.")

    prompt = f"""You are an elite professor and researcher writing a top-tier peer-reviewed manuscript.

Paper Title: "{title}"
Section to Draft: "{section_name}"
Section Objective: {objective}
Key Points to Cover:
{chr(10).join([f"- {b}" for b in bullets]) if bullets else "- Deliver comprehensive coverage of the section theme."}

Target Word Count: approximately {target_words} words.
Writing Tone: {tone}
Problem Statement: {research_insights.get('problem_statement', '')}
Proposed Contribution: {research_insights.get('proposed_contribution', '')}
Available Citations: {', '.join(papers_keys) if papers_keys else "Standard relevant citations."}

Formatting & Quality Directives:
{chr(10).join(formatting_rules)}
- Use formal academic English. Avoid conversational idioms or unsupported hyperbole.
- Ensure all claims are substantiated by theoretical reasoning, mathematical equations, or empirical baselines.
- Write in full continuous prose divided into meaningful logical subsections where appropriate.
"""

    draft = llm_service.generate(
        prompt=prompt,
        system_prompt="You are an author writing a peer-reviewed scientific paper. Write strictly in formal academic LaTeX/Markdown.",
        provider=provider,
        model=model,
        api_key=api_key,
        task_context="section"
    )
    return draft
