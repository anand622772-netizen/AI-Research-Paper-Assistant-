with open(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\generate_perfect_report.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.finditer(r'(add_heading_[123]\([^)]+\)|add_image_figure\([^)]+\))', text)
for m in matches:
    print(m.group(0)[:120])
