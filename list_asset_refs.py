with open(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\generate_perfect_report.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'ASSETS_DIR\s*/\s*"[^"]+"', text)
print(set(matches))
