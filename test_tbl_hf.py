import docx
from docx.oxml import parse_xml

doc = docx.Document()
sec = doc.sections[0]

header_tbl_xml = """<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:tblPr>
    <w:tblW w:w="5000" w:type="pct"/>
    <w:tblBorders>
      <w:bottom w:val="single" w:sz="18" w:space="0" w:color="808080"/>
      <w:insideV w:val="single" w:sz="18" w:space="0" w:color="808080"/>
    </w:tblBorders>
    <w:tblCellMar>
      <w:top w:w="72" w:type="dxa"/>
      <w:left w:w="115" w:type="dxa"/>
      <w:bottom w:w="72" w:type="dxa"/>
      <w:right w:w="115" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
  <w:tblGrid>
    <w:gridCol w:w="8195"/>
    <w:gridCol w:w="1395"/>
  </w:tblGrid>
  <w:tr>
    <w:tc>
      <w:tcPr><w:tcW w:w="8195" w:type="dxa"/></w:tcPr>
      <w:p>
        <w:pPr>
          <w:pStyle w:val="Header"/>
          <w:jc w:val="right"/>
        </w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:sz w:val="20"/>
            <w:color w:val="334155"/>
          </w:rPr>
          <w:t>1. About Department of MScIT</w:t>
        </w:r>
      </w:p>
    </w:tc>
    <w:tc>
      <w:tcPr><w:tcW w:w="1395" w:type="dxa"/></w:tcPr>
      <w:p>
        <w:pPr>
          <w:pStyle w:val="Header"/>
          <w:jc w:val="center"/>
        </w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:b/>
            <w:sz w:val="20"/>
            <w:color w:val="4F81BD"/>
          </w:rPr>
          <w:t>2026 - 2027</w:t>
        </w:r>
      </w:p>
    </w:tc>
  </w:tr>
</w:tbl>"""

footer_tbl_xml = """<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:tblPr>
    <w:tblW w:w="5000" w:type="pct"/>
    <w:tblCellMar>
      <w:top w:w="72" w:type="dxa"/>
      <w:left w:w="115" w:type="dxa"/>
      <w:bottom w:w="72" w:type="dxa"/>
      <w:right w:w="115" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
  <w:tblGrid>
    <w:gridCol w:w="8631"/>
    <w:gridCol w:w="959"/>
  </w:tblGrid>
  <w:tr>
    <w:tc>
      <w:tcPr>
        <w:tcW w:w="4500" w:type="pct"/>
        <w:tcBorders>
          <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tcBorders>
      </w:tcPr>
      <w:p>
        <w:pPr><w:pStyle w:val="Footer"/></w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:sz w:val="19"/>
            <w:color w:val="334155"/>
          </w:rPr>
          <w:t>Minor Project: AI Research Paper Assistant</w:t>
        </w:r>
      </w:p>
    </w:tc>
    <w:tc>
      <w:tcPr>
        <w:tcW w:w="500" w:type="pct"/>
        <w:tcBorders>
          <w:top w:val="single" w:sz="4" w:space="0" w:color="C0504D"/>
        </w:tcBorders>
        <w:shd w:val="clear" w:color="auto" w:fill="943634"/>
      </w:tcPr>
      <w:p>
        <w:pPr>
          <w:pStyle w:val="Header"/>
          <w:jc w:val="center"/>
        </w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:b/>
            <w:sz w:val="19"/>
            <w:color w:val="FFFFFF"/>
          </w:rPr>
          <w:fldChar w:fldCharType="begin"/>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:b/>
            <w:sz w:val="19"/>
            <w:color w:val="FFFFFF"/>
          </w:rPr>
          <w:instrText xml:space="preserve"> PAGE   \* MERGEFORMAT </w:instrText>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:b/>
            <w:sz w:val="19"/>
            <w:color w:val="FFFFFF"/>
          </w:rPr>
          <w:fldChar w:fldCharType="separate"/>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:b/>
            <w:sz w:val="19"/>
            <w:color w:val="FFFFFF"/>
          </w:rPr>
          <w:t>1</w:t>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:b/>
            <w:sz w:val="19"/>
            <w:color w:val="FFFFFF"/>
          </w:rPr>
          <w:fldChar w:fldCharType="end"/>
        </w:r>
      </w:p>
    </w:tc>
  </w:tr>
</w:tbl>"""

# In python-docx, sec.header._element is a <w:hdr>. We clear its children and append the table + an empty paragraph (required by Word)
hdr_el = sec.header._element
hdr_el.clear()
hdr_el.append(parse_xml(header_tbl_xml))
hdr_el.append(parse_xml('<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:pPr><w:pStyle w:val="Header"/></w:pPr></w:p>'))

ftr_el = sec.footer._element
ftr_el.clear()
ftr_el.append(parse_xml(footer_tbl_xml))
ftr_el.append(parse_xml('<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:pPr><w:pStyle w:val="Footer"/></w:pPr></w:p>'))

for i in range(5):
    doc.add_paragraph(f"This is page {i+1} testing the new Header and Footer table structure!")
    if i < 4:
        doc.add_page_break()

doc.save(r"C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\test_tbl_hf.docx")
print("Saved test_tbl_hf.docx successfully!")
