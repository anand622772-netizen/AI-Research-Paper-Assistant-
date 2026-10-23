with open(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\generate_perfect_report.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "INDEX" in l and "def " not in l:
        print("".join(lines[i-5:i+65]))
        break
