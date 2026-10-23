with open(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\generate_perfect_report.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "def setup_new_header_footer" in l:
        print("".join(lines[i+70:i+140]))
        break
