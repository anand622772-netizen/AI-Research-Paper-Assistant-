with open(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\generate_perfect_report.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
pos = text.find("INDEX")
# Find second occurrence (in build_report_doc)
pos2 = text.find("INDEX", pos + 10)
print(text[pos2-100:pos2+1200])
