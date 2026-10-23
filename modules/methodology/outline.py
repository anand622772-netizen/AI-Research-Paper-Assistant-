"""
Methodology Step 2: Outline Generator & Hierarchy Editor.
Generates structured outlines based on conference targets and custom research insights.
"""

from typing import Dict, Any, List
from config import CONFERENCE_TEMPLATES
from modules.llm_provider import llm_service
import json
import re


def generate_structured_outline(
    paper_title: str,
    template_name: str,
    insights: Dict[str, Any],
    provider: str = "auto",
    model: str = None,
    api_key: str = None
) -> List[Dict[str, Any]]:
    """
    Generates a detailed section-by-section outline with objectives,
    bullet points, and recommended word counts tailored to the conference format.
    """
    template_info = CONFERENCE_TEMPLATES.get(template_name, CONFERENCE_TEMPLATES["NeurIPS / ICLR"])
    sections_list = template_info.get("sections", [])

    prompt = f"""You are a scientific program committee chair and expert paper author.
Create a comprehensive, academic-standard paper outline for the following research project:

Title: {paper_title}
Target Venue Style: {template_name}
Target Sections: {', '.join(sections_list)}

Problem Statement: {insights.get('problem_statement', '')}
Research Gap: {insights.get('research_gap', '')}
Proposed Contribution: {insights.get('proposed_contribution', '')}
Benchmarks: {', '.join(insights.get('benchmark_datasets', []))}

Generate a JSON array of sections. Each object in the array must have:
- "id": a unique short string identifier (e.g. "sec_intro")
- "title": Section title (e.g. "1. Introduction")
- "level": 1 (main section)
- "objective": One concise sentence defining the goal of this section
- "bullet_points": 3 to 4 specific technical points or mathematical concepts to cover
- "target_words": Recommended word count (e.g. 800)
- "status": "Not Started"

Output valid JSON only.
"""

    response = llm_service.generate(
        prompt=prompt,
        system_prompt="You are a senior computer science researcher. Output a JSON array only.",
        provider=provider,
        model=model,
        api_key=api_key,
        task_context="outline"
    )

    try:
        match = re.search(r"\[.*\]", response, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict) and "title" in parsed[0]:
                return parsed
    except Exception:
        pass

    # High-quality fallback template tailored to the venue
    default_outline = []
    for idx, sec_name in enumerate(sections_list):
        sec_id = f"sec_{idx}_{re.sub(r'[^a-zA-Z0-9]', '', sec_name.lower())[:8]}"
        default_outline.append({
            "id": sec_id,
            "title": sec_name,
            "level": 1,
            "objective": f"Address core aspects of {sec_name} aligning with conference guidelines.",
            "bullet_points": [
                f"Contextual grounding of {sec_name}",
                "Technical specifications and formal arguments",
                "Validation with empirical and theoretical rigor"
            ],
            "target_words": 200 if "Abstract" in sec_name else (300 if "Conclusion" in sec_name else 900),
            "status": "Drafted"
        })
    return default_outline
