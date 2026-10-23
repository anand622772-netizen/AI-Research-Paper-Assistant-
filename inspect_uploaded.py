import docx
from pathlib import Path

doc1_path = r"C:\Users\anand\.gemini\antigravity\brain\74b7cf38-874d-4c15-8f8f-ab558e9f716d\.user_uploaded\media_1792775134959_43091011.docx"
doc2_path = r"C:\Users\anand\.gemini\antigravity\brain\74b7cf38-874d-4c15-8f8f-ab558e9f716d\.user_uploaded\media_1792775154750_b493f166.docx"
pdf_path = r"C:\Users\anand\.gemini\antigravity\brain\74b7cf38-874d-4c15-8f8f-ab558e9f716d\.user_uploaded\media_1792775127084_0f59e31e.pdf"

d2 = docx.Document(doc2_path)
save_dir = Path(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\doc2_diagrams")
save_dir.mkdir(parents=True, exist_ok=True)

print("DOC 2 parts:")
for rel_id, rel in d2.part.rels.items():
    if "image" in rel.target_ref:
        img_part = rel.target_part
        filename = Path(img_part.partname).name
        out_file = save_dir / f"{rel_id}_{filename}"
        with open(out_file, "wb") as f:
            f.write(img_part.blob)
        print(f"  {rel_id} -> {filename} ({len(img_part.blob)} bytes) -> saved to {out_file.name}")

print("\nParagraphs with images in DOC 2:")
for i, p in enumerate(d2.paragraphs):
    xml = p._element.xml
    if "w:drawing" in xml:
        # extract rel ids
        import re
        rids = re.findall(r'r:embed="([^"]+)"', xml)
        print(f"Para {i}: text='{p.text.strip()}' -> rIds={rids}")
