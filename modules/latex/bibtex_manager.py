"""
BibTeX Manager for AI Research Paper Assistant.
Handles merging, formatting, deduplicating, and validating .bib citation records.
"""

import re
from typing import Dict, List, Set, Tuple


def deduplicate_bibtex(bibtex_str: str) -> str:
    """
    Deduplicates BibTeX entries by citation key and formats them cleanly.
    """
    entries = re.findall(r"(@\w+\s*\{[^@]+)", bibtex_str)
    seen_keys: Set[str] = set()
    unique_entries: List[str] = []

    for entry in entries:
        key_match = re.search(r"@\w+\s*\{\s*([^,]+),", entry)
        if key_match:
            key = key_match.group(1).strip()
            if key not in seen_keys:
                seen_keys.add(key)
                clean_entry = entry.strip()
                if not clean_entry.endswith("}"):
                    clean_entry += "\n}"
                unique_entries.append(clean_entry)
        else:
            unique_entries.append(entry.strip())

    return "\n\n".join(unique_entries)


def extract_keys_from_bibtex(bibtex_str: str) -> List[str]:
    """Returns all entry keys present in the BibTeX text."""
    return re.findall(r"@\w+\s*\{\s*([^,]+),", bibtex_str)


def validate_bibtex_syntax(bibtex_str: str) -> Tuple[bool, List[str]]:
    """
    Validates basic BibTeX syntax.
    Returns (is_valid, error_list).
    """
    errors = []
    if not bibtex_str.strip():
        return True, []

    entries = re.findall(r"@\w+\s*\{[^@]+", bibtex_str)
    if not entries and "@" in bibtex_str:
        errors.append("Unclosed or malformed '@' entry detected in BibTeX.")

    for idx, e in enumerate(entries, 1):
        key_match = re.search(r"@\w+\s*\{\s*([^,]+),", e)
        if not key_match:
            errors.append(f"Entry #{idx} is missing a citation key.")
        if e.count("{") != e.count("}"):
            errors.append(f"Mismatched braces in entry #{idx} ('{key_match.group(1) if key_match else 'unknown'}').")

    return len(errors) == 0, errors
