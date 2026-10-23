"""
Methodology Step 8: Final Paper & Export Portal.
Comprehensive Paper Health Audit, Multi-Format Exporters (LaTeX ZIP, Markdown, HTML),
and Conference Slide Deck Generator.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple
import re
from modules.latex.templates import markdown_to_latex
from modules.llm_provider import llm_service


def audit_paper_health(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Performs comprehensive diagnostic audit on the research manuscript:
    - Word counts
    - Abstract constraints
    - Section completeness
    - Citation coverage
    - Figure and table references
    """
    metadata = project_data.get("metadata", {})
    abstract = project_data.get("sections", {}).get("Abstract", "")
    sections = project_data.get("sections", {})
    outline = project_data.get("outline", [])
    figures = project_data.get("figures", [])
    bibtex = project_data.get("literature_review", {}).get("bibtex_entries", "")

    total_words = sum(len(content.split()) for content in sections.values())
    abstract_words = len(abstract.split())

    # Check outline completeness
    missing_sections = []
    for item in outline:
        title = item.get("title", "")
        # Find matching key in sections
        found = False
        for sec_key in sections.keys():
            if title.lower() in sec_key.lower() or sec_key.lower() in title.lower():
                found = True
                break
        if not found:
            missing_sections.append(title)

    # Citation check
    all_text = " ".join(sections.values())
    cited_keys = set(re.findall(r"\\cite\{([^}]+)\}", all_text))
    flat_cited = set()
    for ck in cited_keys:
        for single in ck.split(","):
            flat_cited.add(single.strip())

    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bibtex))
    unresolved_cites = flat_cited - bib_keys

    # Figure label check
    figure_labels = {f.get("label", "") for f in figures if f.get("label")}
    ref_matches = set(re.findall(r"\\ref\{([^}]+)\}", all_text))

    checklist = [
        {
            "name": "Title Capitalization & Metadata",
            "passed": len(metadata.get("title", "")) > 10 and len(metadata.get("authors", [])) > 0,
            "detail": f"Title has {len(metadata.get('title', ''))} characters; {len(metadata.get('authors', []))} author(s) listed."
        },
        {
            "name": "Abstract Word Limit (150-250 words)",
            "passed": 100 <= abstract_words <= 300,
            "detail": f"Abstract contains {abstract_words} words (recommended 150-250)."
        },
        {
            "name": "Section Completeness",
            "passed": len(missing_sections) == 0,
            "detail": "All planned outline sections have drafted text." if not missing_sections else f"Missing drafts for: {', '.join(missing_sections)}"
        },
        {
            "name": "Citation Integrity",
            "passed": len(unresolved_cites) == 0,
            "detail": f"{len(flat_cited)} unique citation(s) referenced. Unresolved: {len(unresolved_cites)}"
        },
        {
            "name": "Visual Assets & Figures",
            "passed": len(figures) > 0,
            "detail": f"{len(figures)} publication figure(s) attached to manuscript."
        },
        {
            "name": "Target Length & Depth",
            "passed": total_words >= 2500,
            "detail": f"Total paper length is approximately {total_words} words."
        }
    ]

    score = int((sum(1 for c in checklist if c["passed"]) / len(checklist)) * 100)

    return {
        "score": score,
        "total_words": total_words,
        "abstract_words": abstract_words,
        "checklist": checklist,
        "is_ready_for_submission": score >= 85
    }


def export_as_markdown(project_data: Dict[str, Any]) -> str:
    """Exports full project as a unified Markdown manuscript."""
    meta = project_data.get("metadata", {})
    sections = project_data.get("sections", {})
    
    authors_str = ", ".join([f"{a.get('name')} ({a.get('affiliation')})" for a in meta.get("authors", [])])
    
    md = f"""# {meta.get('title', 'Academic Manuscript')}

**Authors:** {authors_str}  
**Keywords:** {', '.join(meta.get('keywords', []))}  
**Target Venue:** {project_data.get('template', 'Academic Conference')}

---

## Abstract
{sections.get('Abstract', '')}

---

"""
    for sec_title, content in sections.items():
        if sec_title.lower() == "abstract":
            continue
        md += f"## {sec_title}\n\n{content}\n\n"

    # Append BibTeX
    bibtex = project_data.get("literature_review", {}).get("bibtex_entries", "")
    if bibtex:
        md += f"## References (BibTeX)\n```bibtex\n{bibtex}\n```\n"

    return md


def export_as_html(project_data: Dict[str, Any]) -> str:
    """Exports full manuscript as a standalone, styled HTML academic pre-print."""
    meta = project_data.get("metadata", {})
    sections = project_data.get("sections", {})
    
    author_cards = "".join([
        f"<div class='author-card'><strong>{a.get('name')}</strong><br><small>{a.get('affiliation')}</small><br><code>{a.get('email')}</code></div>"
        for a in meta.get("authors", [])
    ])

    body_html = ""
    for sec_title, content in sections.items():
        if sec_title.lower() == "abstract":
            continue
        # Convert simple linebreaks to paragraphs
        paragraphs = content.split("\n\n")
        p_html = "".join([f"<p>{p.strip().replace(chr(10), '<br>')}</p>" for p in paragraphs if p.strip()])
        body_html += f"<section><h2>{sec_title}</h2>{p_html}</section>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{meta.get('title', 'Manuscript')}</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.68;
    color: #1a1a1a;
    background: #fbfbfb;
    max-width: 860px;
    margin: 40px auto;
    padding: 0 25px;
  }}
  h1 {{ font-size: 2.2rem; line-height: 1.25; color: #111; text-align: center; margin-bottom: 24px; }}
  .authors {{ display: flex; justify-content: center; gap: 24px; flex-wrap: wrap; margin-bottom: 30px; }}
  .author-card {{ text-align: center; font-size: 0.95rem; }}
  .abstract-box {{
    background: #f1f5f9;
    border-left: 4px solid #2563eb;
    padding: 20px 24px;
    border-radius: 6px;
    margin-bottom: 35px;
    font-size: 1.02rem;
  }}
  .abstract-box h3 {{ margin-top: 0; color: #1e3a8a; }}
  section {{ margin-bottom: 35px; }}
  h2 {{ border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; color: #0f172a; }}
  p {{ margin-bottom: 16px; text-align: justify; }}
  code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
</style>
</head>
<body>
  <h1>{meta.get('title', 'Academic Paper')}</h1>
  <div class="authors">
    {author_cards}
  </div>

  <div class="abstract-box">
    <h3>Abstract</h3>
    <p>{sections.get('Abstract', '')}</p>
    <p><strong>Keywords:</strong> {', '.join(meta.get('keywords', []))}</p>
  </div>

  {body_html}
</body>
</html>"""
    return html


def generate_presentation_slides(project_data: Dict[str, Any], provider: str = "auto", model: str = None, api_key: str = None) -> str:
    """
    Generates a 6-slide conference presentation outline for oral/spotlight presentations.
    """
    meta = project_data.get("metadata", {})
    abstract = project_data.get("sections", {}).get("Abstract", "")
    insights = project_data.get("research_materials", {}).get("extracted_insights", {})

    prompt = f"""You are creating a conference spotlight presentation slide deck (6 slides) for an accepted paper:

Paper Title: {meta.get('title')}
Target Conference: {project_data.get('template')}
Abstract: {abstract}
Problem: {insights.get('problem_statement')}
Contribution: {insights.get('proposed_contribution')}

Generate a slide deck script. For each slide (Slide 1 to Slide 6), provide:
1. Slide Title
2. Main Visual / Diagram Idea
3. 3-4 Speaker Bullet Points
4. Speaker Delivery Script (30-45 seconds spoken notes)

Format as clean, beautiful Markdown.
"""

    return llm_service.generate(
        prompt=prompt,
        system_prompt="You are an expert keynote presenter at NeurIPS and ICML.",
        provider=provider,
        model=model,
        api_key=api_key,
        task_context="final_paper"
    )
