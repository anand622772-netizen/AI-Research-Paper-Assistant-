import docx

doc2_path = r"C:\Users\anand\.gemini\antigravity\brain\74b7cf38-874d-4c15-8f8f-ab558e9f716d\.user_uploaded\media_1792775154750_b493f166.docx"
d2 = docx.Document(doc2_path)

for i, p in enumerate(d2.paragraphs):
    txt = p.text.strip()
    xml = p._element.xml
    has_img = "w:drawing" in xml
    if has_img or (txt and len(txt) > 0 and (txt.startswith("Figure") or txt.startswith("4.") or txt.startswith("3.") or txt.startswith("Data"))):
        print(f"P{i} [img={has_img}]: {txt[:90]}")
