with open(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\generate_perfect_report.py", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("index_items_spec = [")
print(text[pos:pos+2500])
