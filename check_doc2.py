import docx
import re

d2 = docx.Document(r"C:\Users\anand\.gemini\antigravity\brain\74b7cf38-874d-4c15-8f8f-ab558e9f716d\.user_uploaded\media_1792775154750_b493f166.docx")
for i, p in enumerate(d2.paragraphs):
    for j, r in enumerate(p.runs):
        if "w:drawing" in r._element.xml:
            rids = re.findall(r'r:embed="([^"]+)"', r._element.xml)
            print(f"Para {i} Run {j}: text={repr(r.text)} rids={rids}")
