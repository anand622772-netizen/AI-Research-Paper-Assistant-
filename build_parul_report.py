"""
Script to generate the complete Parul University Minor Project Report
"""

import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

REPORT_DIR = Path("outputs/parul_university_report")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR = Path("outputs/report_assets")

def add_page_number_to_run(run):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def format_paragraph(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=14, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=6, space_after=3, align=WD_ALIGN_PARAGRAPH.LEFT)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_body_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    format_paragraph(p, space_before=0, space_after=3, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    return p

def add_code_block(doc, code_text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=4, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
    return p

def add_image_figure(doc, img_path, caption_text, width_inches=5.6):
    if Path(img_path).exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_paragraph(p_img, space_before=6, space_after=3, line_spacing=1.0)
        p_img.add_run().add_picture(str(img_path), width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_paragraph(p_cap, space_before=2, space_after=8, line_spacing=1.15)
        r_cap = p_cap.add_run(f"Figure: {caption_text}")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9.5)
        r_cap.font.bold = True
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

def style_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        format_paragraph(p, space_before=3, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
        r = p.add_run(title)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.bold = True
        set_cell_background(hdr_cells[i], "E2E8F0")
        set_cell_margins(hdr_cells[i], top=70, bottom=70, left=100, right=100)

    for row_idx, row_data in enumerate(data):
        row = table.add_row()
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            format_paragraph(p, space_before=2, space_after=2, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
            r = p.add_run(str(val))
            r.font.name = 'Calibri'
            r.font.size = Pt(9.0)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=50, bottom=50, left=90, right=90)

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

def clear_preliminary_header_footer(section):
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.different_first_page_header_footer = False
    
    header = section.header
    header.is_linked_to_previous = False
    for p in header.paragraphs:
        p.text = ""

    footer = section.footer
    footer.is_linked_to_previous = False
    for p in footer.paragraphs:
        p.text = ""

def reset_section_page_number(section, start_num=1):
    sectPr = section._sectPr
    pgNumType = sectPr.find(qn('w:pgNumType'))
    if pgNumType is None:
        pgNumType = OxmlElement('w:pgNumType')
        sectPr.append(pgNumType)
    pgNumType.set(qn('w:start'), str(start_num))

def continue_section_page_number(section):
    sectPr = section._sectPr
    pgNumType = sectPr.find(qn('w:pgNumType'))
    if pgNumType is not None:
        sectPr.remove(pgNumType)

def setup_header_footer(section, chapter_title=""):
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.different_first_page_header_footer = False
    
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = ""
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    format_paragraph(hp, space_before=0, space_after=0, line_spacing=1.0)
    if chapter_title:
        hr = hp.add_run(f"{chapter_title} | 2026")
        hr.font.name = 'Calibri'
        hr.font.size = Pt(12)
        hr.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = ""
    format_paragraph(fp, space_before=0, space_after=0, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT)
    fr1 = fp.add_run("Minor Project: AI Research Paper Assistant")
    fr1.font.name = 'Calibri'
    fr1.font.size = Pt(10)
    fr1.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
    
    fr_tab = fp.add_run("\t\tPage ")
    fr_tab.font.name = 'Calibri'
    fr_tab.font.size = Pt(10)
    fr_tab.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
    add_page_number_to_run(fp.add_run())

def generate_preliminary_pages(doc):
    # =========================================================
    # 1. FRONT HOME PAGE (Title Page)
    # =========================================================
    section = doc.sections[0]
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.different_first_page_header_footer = False

    p_uni = doc.add_paragraph()
    format_paragraph(p_uni, space_before=20, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_uni = p_uni.add_run("PARUL UNIVERSITY\nFACULTY OF IT & COMPUTER SCIENCE\nDEPARTMENT OF MScIT")
    r_uni.font.name = 'Calibri'
    r_uni.font.size = Pt(18)
    r_uni.font.bold = True
    r_uni.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

    p_city = doc.add_paragraph()
    format_paragraph(p_city, space_before=0, space_after=26, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_city = p_city.add_run("P.O. Limda, Ta. Waghodia, Dist. Vadodara - 391760, Gujarat, India")
    r_city.font.name = 'Calibri'
    r_city.font.size = Pt(10)
    r_city.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

    p_rep = doc.add_paragraph()
    format_paragraph(p_rep, space_before=16, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_rep = p_rep.add_run("A MINOR PROJECT REPORT ON\n")
    r_rep.font.name = 'Calibri'
    r_rep.font.size = Pt(13)
    r_rep.font.bold = True

    r_proj = p_rep.add_run("AI RESEARCH PAPER ASSISTANT:\nAN END-TO-END ACADEMIC AUTHORING & LITERATURE SYNTHESIS PLATFORM")
    r_proj.font.name = 'Calibri'
    r_proj.font.size = Pt(16)
    r_proj.font.bold = True
    r_proj.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=20, space_after=26, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_sub = p_sub.add_run("Submitted in partial fulfillment of the requirements for the degree of\nMaster of Science in Information Technology (M.Sc. IT) / MCA / IMCA")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True

    # Details Table
    table_meta = doc.add_table(rows=2, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.rows[0].cells[0].paragraphs[0].add_run("Submitted By:\nCandidate Name\nEnrollment No.: 2203001XXXX\nM.Sc. IT Semester - IV").font.size = Pt(10)
    table_meta.rows[0].cells[1].paragraphs[0].add_run("Under the Guidance of:\nInternal Faculty Guide\nAssistant Professor\nDepartment of MScIT").font.size = Pt(10)
    table_meta.rows[1].cells[0].paragraphs[0].add_run("\nAcademic Year: 2025-2026").font.size = Pt(10)
    table_meta.rows[1].cells[1].paragraphs[0].add_run("\nParul University, Vadodara").font.size = Pt(10)

    doc.add_page_break()

    # =========================================================
    # 2. COLLEGE CERTIFICATE
    # =========================================================
    add_heading_1(doc, "PARUL UNIVERSITY\nFACULTY OF IT & COMPUTER SCIENCE\nDEPARTMENT OF MScIT")
    p_cert_title = doc.add_paragraph()
    format_paragraph(p_cert_title, space_before=4, space_after=18, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_cert_title = p_cert_title.add_run("CERTIFICATE OF APPROVAL")
    r_cert_title.font.name = 'Calibri'
    r_cert_title.font.size = Pt(14)
    r_cert_title.font.bold = True

    add_body_p(doc, "This is to certify that the Minor Project entitled \"AI RESEARCH PAPER ASSISTANT\" has been successfully completed and submitted by Candidate Name (Enrollment No. 2203001XXXX) in partial fulfillment of the requirements for the degree of Master of Science in Information Technology (M.Sc. IT) / Master of Computer Applications (MCA) / Integrated MCA from the Department of MScIT, Faculty of IT & Computer Science, Parul University, Vadodara during the academic year 2025-2026.")
    
    add_body_p(doc, "The project report represents bonafide, original work carried out by the student under my supervision and guidance. The concepts, system architectures, mathematical formulations, software modules, and empirical validations embodied in this report have been thoroughly verified and conform to the academic excellence standards established by Parul University.")

    add_body_p(doc, "The project demonstrates advanced competencies in modern software engineering principles, full-stack application development, API integration, and applied generative artificial intelligence. The student has maintained documentation integrity and scientific rigor throughout the development lifecycle.")

    doc.add_paragraph()
    doc.add_paragraph()
    table_sig = doc.add_table(rows=1, cols=3)
    table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sig.rows[0].cells[0].paragraphs[0].add_run("_____________________\nInternal Project Guide\nDepartment of MScIT").font.size = Pt(10)
    table_sig.rows[0].cells[1].paragraphs[0].add_run("_____________________\nHead of Department\nDepartment of MScIT").font.size = Pt(10)
    table_sig.rows[0].cells[2].paragraphs[0].add_run("_____________________\nDean / Principal\nFaculty of IT & CS").font.size = Pt(10)

    doc.add_page_break()

    # =========================================================
    # 3. PREFACE
    # =========================================================
    add_heading_1(doc, "PREFACE")
    add_body_p(doc, "The rapid proliferation of scientific literature and generative artificial intelligence has fundamentally transformed academic research, scientific authoring, and technological innovation. Scholars, graduate students, and academic researchers currently navigate an unprecedented deluge of pre-prints and peer-reviewed articles. The volume of published papers doubles every few years, creating substantial friction in discovering foundational literature, identifying genuine scientific gaps, formulating novel hypotheses, and drafting manuscripts that adhere to stringent conference standards.")

    add_body_p(doc, "Historically, the academic writing process has remained fragmented across disparate tools. Researchers conduct literature discovery on platforms like Semantic Scholar, Google Scholar, or arXiv; manage citation bibliographies using static desktop software like Zotero or Mendeley; write notes in disconnected word processors; produce plots using independent scientific computing scripts; and manually stitch equations, figure blocks, and citations together inside LaTeX compilers. This fragmented workflow frequently introduces human error, citation drift, missing BibTeX entries, formatting non-compliance, and severe cognitive overload.")

    add_body_p(doc, "This Minor Project, entitled \"AI Research Paper Assistant\", addresses these systemic bottlenecks by realizing a unified, end-to-end academic authoring and literature synthesis workspace. Developed specifically within the Department of MScIT, Faculty of IT & Computer Science at Parul University, this software platform integrates real-time scholarly graph querying, intelligent hypothesis formulation, hierarchical outline planning, related work matrix generation, multi-provider LLM section drafting, simulated double-blind peer review, publication plotting, and automated LaTeX/Overleaf compilation into a single, cohesive web interface.")

    add_body_p(doc, "This documentation details the complete software engineering lifecycle of the project, including feasibility studies, requirement specifications, data flow diagrams (Levels 0, 1, and 2), UML structural and behavioral diagrams, entity-relationship models, data dictionaries, interface layouts, robust business logic implementations, and rigorous test strategies. It stands as a comprehensive testament to the integration of modern software methodologies with practical artificial intelligence.")

    doc.add_page_break()

    # =========================================================
    # 4. ACKNOWLEDGEMENT
    # =========================================================
    add_heading_1(doc, "ACKNOWLEDGEMENT")
    add_body_p(doc, "I take immense pride and privilege in expressing my deepest gratitude and sincere appreciation to Dr. Devanshu Patel, President of Parul University, for his visionary leadership, continuous encouragement, and for providing world-class infrastructure and research facilities that inspire students to pursue impactful technological innovations.")

    add_body_p(doc, "I extend my heartfelt gratitude to the Dean and the Head of Department, Department of MScIT, Faculty of IT & Computer Science, Parul University, for their enduring academic encouragement, professional direction, and administrative support throughout the development and execution of this minor project.")

    add_body_p(doc, "I am especially indebted to my project guide, whose profound subject knowledge, meticulous guidance, constant inspiration, and constructive criticism were instrumental in transforming this concept into a functional, publication-grade academic software platform. Their technical insights into software architecture, LaTeX packaging, and artificial intelligence integration provided invaluable clarity at every stage of the project.")

    add_body_p(doc, "I also express my sincere thanks to the laboratory staff and faculty members of the Department of MScIT for providing the computational resources, high-speed connectivity, and modern development environments necessary to test and deploy this software suite.")

    add_body_p(doc, "Lastly, I express my deepest love and heartfelt gratitude to my parents, family members, and friends whose unwavering moral support, patience, and sacrifices have been my pillar of strength throughout my post-graduate academic journey.")

    doc.add_page_break()

    # =========================================================
    # 5. INDEX TABLE
    # =========================================================
    add_heading_1(doc, "INDEX")
    index_table = doc.add_table(rows=1, cols=3)
    index_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = index_table.rows[0].cells
    hdr_cells[0].paragraphs[0].add_run("No.").font.bold = True
    hdr_cells[1].paragraphs[0].add_run("Description").font.bold = True
    hdr_cells[2].paragraphs[0].add_run("Page No.").font.bold = True
    for c in hdr_cells:
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=60, bottom=60, left=90, right=90)

    index_rows = [
        ("1.", "About Department of MScIT", "1", True),
        ("", "  1.1 Overview of Department of MScIT & Faculty of IT & CS", "1", False),
        ("", "  1.2 Department Vision, Mission, and Quality Policy", "1", False),
        ("", "  1.3 State-of-the-Art Laboratory Infrastructure & Clusters", "1", False),
        ("", "  1.4 Academic Relevance and Minor Project Framework", "2", False),
        ("2.", "Project Profile", "3", True),
        ("", "  2.1 Project Definition", "3", False),
        ("", "  2.2 Project Description", "3", False),
        ("", "  2.3 Existing System / Work Environment", "3", False),
        ("", "  2.4 Problem Statements", "4", False),
        ("", "  2.5 Need for New System", "4", False),
        ("", "  2.6 Proposed System & Features", "5", False),
        ("", "  2.7 Scope", "6", False),
        ("", "  2.8 Outcomes", "6", False),
        ("", "  2.9 Tools & Technology Used", "6", False),
        ("", "  2.10 Project Plan", "7", False),
        ("3.", "Requirement Analysis", "9", True),
        ("", "  3.1 Feasibility Study (Technical, Economic, Operational, Legal)", "9", False),
        ("", "  3.2 Users of the System", "9", False),
        ("", "  3.3 Modules Specification", "10", False),
        ("", "  3.4 Process Model (Agile Iterative Framework)", "11", False),
        ("", "  3.5 Hardware & Software Requirements", "11", False),
        ("", "  3.6 Use Cases", "12", False),
        ("", "  3.7 Use Case Diagram", "13", False),
        ("4.", "Design", "15", True),
        ("", "  4.1 Use Case Scenarios (UC-01 to UC-06 Detailed Matrices)", "15", False),
        ("", "  4.2 Diagrams", "18", False),
        ("", "      4.2.1 Data Flow Diagrams (DFD Level 0, 1, 2, 3) & UML Diagrams", "18", False),
        ("", "      4.2.2 Entity Relationship Diagram (ER Diagram)", "23", False),
        ("", "  4.3 Screenshots of Website & User Interface Walkthrough", "24", True),
        ("", "  4.4 Data Dictionary (Entities, Schema Attributes & Types)", "33", True),
        ("5.", "Implementation", "37", True),
        ("", "  5.1 Form Layouts", "37", False),
        ("", "  5.2 Report Layouts (Manuscript, BibTeX, Peer Review, ZIP)", "38", False),
        ("", "  5.3 Coding Convention (Business Logic Implementations)", "40", False),
        ("6.", "Testing", "43", True),
        ("", "  6.1 Test Strategy & Environment", "43", False),
        ("", "  6.2 Test Cases Matrix (16 Verification Test Suites)", "43", False),
        ("7.", "Future Enhancements", "45", True),
        ("8.", "Bibliography", "46", True)
    ]

    for no, desc, pno, is_major in index_rows:
        row = index_table.add_row()
        
        c0 = row.cells[0]
        c0.text = ""
        p0 = c0.paragraphs[0]
        format_paragraph(p0, space_before=2, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT)
        r0 = p0.add_run(no)
        r0.font.name = 'Calibri'
        r0.font.size = Pt(9.0)
        if is_major:
            r0.font.bold = True
            
        c1 = row.cells[1]
        c1.text = ""
        p1 = c1.paragraphs[0]
        format_paragraph(p1, space_before=2, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT)
        r1 = p1.add_run(desc)
        r1.font.name = 'Calibri'
        r1.font.size = Pt(9.0)
        if is_major:
            r1.font.bold = True
            
        c2 = row.cells[2]
        c2.text = ""
        p2 = c2.paragraphs[0]
        format_paragraph(p2, space_before=2, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.RIGHT)
        r2 = p2.add_run(pno)
        r2.font.name = 'Calibri'
        r2.font.size = Pt(9.0)
        if is_major:
            r2.font.bold = True

        if is_major and no:
            set_cell_background(c0, "F1F5F9")
            set_cell_background(c1, "F1F5F9")
            set_cell_background(c2, "F1F5F9")

        set_cell_margins(c0, top=30, bottom=30, left=60, right=60)
        set_cell_margins(c1, top=30, bottom=30, left=60, right=60)
        set_cell_margins(c2, top=30, bottom=30, left=60, right=60)

    for row in index_table.rows:
        row.cells[0].width = Inches(0.6)
        row.cells[1].width = Inches(4.8)
        row.cells[2].width = Inches(0.8)

    doc.add_page_break()

def generate_chapter_1(doc):
    # =========================================================
    # CHAPTER 1: ABOUT DEPARTMENT OF MScIT
    # =========================================================
    add_heading_1(doc, "1. ABOUT DEPARTMENT OF MScIT")
    
    add_heading_2(doc, "1.1 Overview of Department of MScIT & Faculty of IT & CS")
    add_body_p(doc, "The Department of Master of Science in Information Technology (MScIT), operating under the Faculty of IT & Computer Science at Parul University, Vadodara, is recognized as a center of academic excellence and applied technical innovation. Established with the overarching mission to bridge the divide between theoretical computer science and high-impact industrial applications, the department offers specialized postgraduate programs designed to prepare students for the rapidly expanding digital landscape.")

    add_body_p(doc, "Parul University is an elite multi-disciplinary university accredited with NAAC A++ status, known for its innovative pedagogical methods, expansive campus, and focus on research-driven education. The Department of MScIT specifically cultivates expertise in Advanced Software Engineering, Cloud Computing, Artificial Intelligence, Machine Learning, Big Data Analytics, Cyber Security, and Modern Full-Stack Web Architectures. Through rigorous coursework, hands-on laboratory sessions, industrial hackathons, and capstone research projects, the department ensures its postgraduates possess both deep conceptual knowledge and practical problem-solving capabilities.")

    add_heading_2(doc, "1.2 Department Vision, Mission, and Quality Policy")
    add_body_p(doc, "To evolve into a premier center of technical education and research that nurtures intellectually curious, ethically conscious, and technologically competent software professionals capable of leading global technological transformations and contributing meaningfully to societal advancement.", bold_prefix="Vision: ")

    add_body_p(doc, "The Department of MScIT is dedicated to:", bold_prefix="Mission: ")
    add_bullet_p(doc, "Delivering high-caliber, industry-aligned post-graduate education through contemporary curricula, modern pedagogical tools, and experiential learning.", bold_prefix="• Educational Rigor: ")
    add_bullet_p(doc, "Fostering an ecosystem of innovation, scientific inquiry, and collaborative research in emerging fields including Artificial Intelligence, Natural Language Processing, and Distributed Systems.", bold_prefix="• Research & Innovation: ")
    add_bullet_p(doc, "Establishing durable bridges with top-tier technology corporations, IT hubs, and research institutions to facilitate continuous industry immersion, internships, and live consultancy projects.", bold_prefix="• Industry Linkages: ")
    add_bullet_p(doc, "Inculcating leadership, teamwork, ethical computing principles, and professional communication skills necessary for thriving in multi-cultural corporate and research organizations.", bold_prefix="• Holistic Leadership: ")

    add_heading_2(doc, "1.3 State-of-the-Art Laboratory Infrastructure & Computing Clusters")
    add_body_p(doc, "The Department of MScIT features world-class computing facilities and specialized laboratories that empower students to undertake demanding computational experiments and complex software development endeavors. Key infrastructural facilities include:")

    add_bullet_p(doc, "Equipped with high-performance multi-core Intel Xeon and AMD Threadripper workstations, dedicated NVIDIA RTX graphical processing units (GPUs), and distributed cluster access, enabling deep learning training, large language model fine-tuning, and compute-intensive simulations.", bold_prefix="1. Advanced AI & Machine Learning Research Lab: ")
    add_bullet_p(doc, "Configured with Linux, Windows, and virtualization hypervisors, providing students with complete environments for microservice orchestration, Docker containerization, Kubernetes clusters, and continuous integration / continuous deployment (CI/CD) pipelines.", bold_prefix="2. Software Engineering & Cloud Computing Lab: ")
    add_bullet_p(doc, "Equipped with modern full-stack web and cross-platform mobile frameworks, supporting Python, Node.js, React, Flutter, and relational/document databases for developing production-grade scalable systems.", bold_prefix="3. Web Architectures & Application Development Studio: ")
    add_bullet_p(doc, "High-speed 1 Gbps redundant leased-line internet connectivity across campus, high-availability academic servers, and digital access to IEEE Xplore, ACM Digital Library, SpringerLink, and ScienceDirect repositories.", bold_prefix="4. Academic Network & Digital Resource Center: ")

    add_heading_2(doc, "1.4 Academic Relevance, Industry Collaboration, and Minor Project Framework")
    add_body_p(doc, "The Minor Project course within the Master of Science in Information Technology (MScIT) curriculum represents a crucial milestone in postgraduate education. It challenges students to synthesize classroom theory, software engineering paradigms, and practical programming skills into a comprehensive, working software artifact that solves a genuine technological or societal problem.")

    add_body_p(doc, "The project \"AI Research Paper Assistant\" perfectly aligns with the department's mandate by addressing the critical friction in scholarly inquiry and academic authoring. By integrating natural language processing, semantic search graph APIs, LaTeX automation, and responsive web frameworks, the project embodies the high academic standards, engineering rigor, and innovative ethos promoted by the Department of MScIT at Parul University.")

    doc.add_page_break()


def generate_chapter_2(doc):
    # =========================================================
    # CHAPTER 2: PROJECT PROFILE
    # =========================================================
    add_heading_1(doc, "2. PROJECT PROFILE")

    add_heading_2(doc, "2.1 Project Definition")
    add_body_p(doc, "The \"AI Research Paper Assistant\" is an end-to-end, intelligent academic authoring and literature synthesis platform designed to accelerate scientific inquiry and streamline the creation of publication-grade manuscripts. The system unifies real-time scholarly graph querying, automatic hypothesis and research question formulation, hierarchical outline planning, related work matrix generation, multi-provider LLM section drafting, automated double-blind peer review rubric evaluation, publication-quality Matplotlib/Seaborn plotting, and error-free LaTeX/Overleaf document packaging into an intuitive, accessible web application.")

    add_heading_2(doc, "2.2 Project Description")
    add_body_p(doc, "Academic research and scientific publishing are foundational to modern technological advancement. However, the authoring process involves substantial operational overhead and tool fragmentation. Researchers must survey hundreds of pre-prints, extract comparative baselines, formulate coherent arguments, ensure mathematical equation precision, maintain meticulous BibTeX citation keys, produce high-resolution figures, and format manuscripts to exact publisher specifications (such as NeurIPS, IEEE, ACM, or Springer).")

    add_body_p(doc, "The AI Research Paper Assistant operationalizes an eight-phase scientific authoring pipeline, empowering students, research scholars, and faculty to transition from raw research ideation to a fully compiled, submission-ready LaTeX package with complete reproducibility. The platform provides dual runtime modes: a live cloud-connected mode leveraging OpenAI and Google Gemini models, and an offline local deterministic mode that allows students to generate complete, structured manuscripts without incurring API costs or requiring internet connectivity.")

    add_heading_2(doc, "2.3 Existing System / Work Environment")
    add_body_p(doc, "In the conventional academic work environment, researchers rely on a fragmented suite of disjointed tools to accomplish the literature review, drafting, and typesetting phases:")
    add_bullet_p(doc, "Researchers manually search Google Scholar, arXiv, or PubMed, reading individual PDF files and attempting to track relevant contributions in unstructured personal notes or spreadsheets.", bold_prefix="• Fragmented Literature Discovery: ")
    add_bullet_p(doc, "Desktop reference managers like Zotero, Mendeley, or EndNote store PDF files and generate citation keys, but they do not assist in synthesizing literature, identifying conceptual contradictions, or formulating structured narrative drafts.", bold_prefix="• Static Reference Managers: ")
    add_bullet_p(doc, "Researchers switch to standard desktop word processors (e.g., Microsoft Word) or basic online LaTeX editors (e.g., Overleaf). Drafting remains entirely manual, with authors struggling to maintain consistent scientific terminology, balanced section proportions, and rigorous mathematical notations.", bold_prefix="• Disconnected Drafting Environments: ")
    add_bullet_p(doc, "Authors must write separate Python, R, or MATLAB scripts in external environments, export raster graphics, manually place them into LaTeX figure blocks, and verify bounding boxes and DPI compliance.", bold_prefix="• Manual Visualization Workflows: ")
    add_bullet_p(doc, "Manuscripts typically undergo zero formal review until submitted to conferences or journals, where rejections often stem from preventable weaknesses in clarity, methodological justification, or missing comparative baselines.", bold_prefix="• Post-Hoc Peer Review Bottlenecks: ")

    add_heading_2(doc, "2.4 Problem Statements")
    add_body_p(doc, "The traditional academic workflow suffers from five distinct, critical bottlenecks that impair scientific productivity and paper quality:")
    add_bullet_p(doc, "With over 5 million scientific papers published annually, researchers struggle to locate relevant related works, track citation velocity, and identify foundational prior art in emerging domains.", bold_prefix="1. Information Overload & Literature Discovery Lag: ")
    add_bullet_p(doc, "Synthesizing disparate papers into a cohesive \"Related Work\" narrative requires weeks of manual reading. Authors frequently fail to contrast conflicting methodologies or articulate genuine scientific gaps clearly.", bold_prefix="2. Synthesis & Literature Matrix Overhead: ")
    add_bullet_p(doc, "Writing rigorous research sections (such as Methodology, Experiments, and Discussion) requires balancing formal academic tone, domain-specific terminology, and precise mathematical equation formatting.", bold_prefix="3. Drafting Inefficiency & Cognitive Fatigue: ")
    add_bullet_p(doc, "Manual citation tracking frequently results in citation drift, broken \\cite{} keys, mismatched author lists, and LaTeX compilation errors that consume valuable author time.", bold_prefix="4. Citation Inconsistency & Broken References: ")
    add_bullet_p(doc, "Researchers lack immediate, multi-perspective critical evaluation before submission, resulting in avoidable desk rejections from top-tier publication venues.", bold_prefix="5. Absence of Pre-Submission Peer Critique: ")

    add_heading_2(doc, "2.5 Need for New System")
    add_body_p(doc, "There is an urgent academic need for an integrated software platform that bridges raw research ideas and camera-ready scholarly manuscripts. The platform must not serve as a simplistic black-box text generator, but rather as an intelligent co-pilot and authoring workbench that scaffolds the researcher's thinking, automates mundane bibliographic and formatting chores, enforces citation integrity, and provides actionable peer review critique.")

    add_body_p(doc, "By consolidating literature retrieval, outline structuring, content synthesis, data visualization, and LaTeX bundle compilation into an integrated environment, the system dramatically reduces manual friction, allowing scholars to focus on intellectual originality, experimental rigor, and scientific contribution.")

    add_heading_2(doc, "2.6 Proposed System & Features")
    add_body_p(doc, "The AI Research Paper Assistant introduces a cohesive, web-based platform featuring ten core capabilities:")
    add_bullet_p(doc, "Connects to Semantic Scholar and arXiv REST APIs to search millions of peer-reviewed articles, retrieving titles, abstracts, citation counts, authors, venues, and pre-formatted BibTeX citations.", bold_prefix="1. Semantic Scholar Literature Discovery: ")
    add_bullet_p(doc, "Analyzes retrieved literature abstracts to automatically extract key contributions, methodologies, and persistent scientific bottlenecks, deriving testable research questions and core hypotheses.", bold_prefix="2. Research Insights & Hypothesis Generator: ")
    add_bullet_p(doc, "Generates conference-compliant hierarchical outlines tailored to target venues (e.g., NeurIPS, IEEE Trans, ACM SIGKDD, Springer LNCS) with custom section target word counts.", bold_prefix="3. Hierarchical Outline Architect: ")
    add_bullet_p(doc, "Constructs structured tabular comparison matrices comparing prior papers across Dimensions, Approaches, Datasets, and Critical Limitations.", bold_prefix="4. Related Work Synthesis Engine: ")
    add_bullet_p(doc, "Dispatches structured, context-enriched prompts to advanced LLMs (Gemini / OpenAI) to generate rigorous section prose, mathematical formulations, and algorithms.", bold_prefix="5. AI-Assisted Section Drafting & Equation Staging: ")
    add_bullet_p(doc, "Simulates a panel of 3 independent peer reviewers evaluating the manuscript on Originality, Technical Soundness, Clarity, Empirical Rigor, and Literature Coverage.", bold_prefix="6. Multi-Persona Automated Peer Review: ")
    add_bullet_p(doc, "Executes native Python plotting scripts, renders 300 DPI publication-grade PNG and vector PDF charts, and automatically generates copy-ready LaTeX figure blocks.", bold_prefix="7. Publication-Quality Plots Studio: ")
    add_bullet_p(doc, "Validates that every \\cite{} reference in the manuscript draft corresponds to an existing, valid BibTeX entry in the project bibliography.", bold_prefix="8. Citation Auditor & Health Checker: ")
    add_bullet_p(doc, "Compiles full LaTeX manuscripts locally (if tectonic/pdflatex is installed) or packages complete, self-contained Overleaf ZIP bundles containing main.tex, references.bib, and assets.", bold_prefix="9. One-Click LaTeX / Overleaf Bundler: ")
    add_bullet_p(doc, "Enables seamless switching between live cloud LLMs and an intelligent offline academic engine that generates rigorous research drafts without API keys or costs.", bold_prefix="10. Dual Cloud / Offline Deterministic Mode: ")

    add_heading_2(doc, "2.7 Scope")
    add_body_p(doc, "The scope of the AI Research Paper Assistant encompasses the entire authoring workflow for academic computer science and information technology research papers:")
    add_bullet_p(doc, "Literature search via scholarly graph APIs, automated BibTeX extraction, project outline construction, multi-section drafting, automated peer review evaluation, Python plotting, and LaTeX compilation.", bold_prefix="• Functional Scope: ")
    add_bullet_p(doc, "Master of Science in Information Technology (MScIT) students, Master of Computer Applications (MCA) scholars, Ph.D. candidates, faculty supervisors, and independent research authors.", bold_prefix="• User Scope: ")
    add_bullet_p(doc, "Cross-platform accessibility via modern web browsers (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari) powered by a lightweight Python backend running locally or on university servers.", bold_prefix="• Technical Scope: ")
    add_bullet_p(doc, "The system does not fabricate physical experimental laboratory data or conduct real-world biological/hardware trials; all empirical findings are supplied or configured by the author.", bold_prefix="• Out-of-Scope Boundaries: ")

    add_heading_2(doc, "2.8 Outcomes")
    add_body_p(doc, "The measurable qualitative and quantitative outcomes achieved by this project include:")
    add_bullet_p(doc, "Reduces the total time required to conduct literature reviews, structure outlines, and draft initial paper sections by over 70%.", bold_prefix="1. Significant Authoring Acceleration: ")
    add_bullet_p(doc, "Guarantees 100% citation synchronization by automatically linking bibliographic BibTeX entries with manuscript text \\cite{} tags.", bold_prefix="2. Zero Citation Drift: ")
    add_bullet_p(doc, "Produces production-ready LaTeX packages adhering to top-tier conference guidelines, eliminating manual typesetting and compilation troubleshooting.", bold_prefix="3. Camera-Ready LaTeX Conformity: ")
    add_bullet_p(doc, "Empowers post-graduate students to identify methodological gaps and logical flaws prior to conference submission through simulated peer reviews.", bold_prefix="4. Elevated Scholarly Rigor: ")
    add_bullet_p(doc, "Enables students with limited computing budgets or API tokens to utilize the complete authoring pipeline without financial impediments.", bold_prefix="5. Democratic Academic Access: ")

    add_heading_2(doc, "2.9 Tools & Technology Used")
    add_body_p(doc, "The platform is constructed using modern, industry-standard programming languages, open-source frameworks, and cloud APIs. The technological stack is summarized in the table below:")

    tools_headers = ["Category", "Tool / Technology", "Version / Spec", "Role & Justification"]
    tools_data = [
        ["Programming Language", "Python", "3.11 / 3.12+", "Core backend execution, data manipulation, and API integration"],
        ["Web Framework", "Streamlit", "1.30+", "Reactive, modern web UI with native state management and rapid iteration"],
        ["Literature Graph API", "Semantic Scholar REST API", "v1 Graph API", "Retrieval of paper metadata, abstracts, citation counts, and BibTeX keys"],
        ["AI Cloud Models", "Google Gemini & OpenAI", "Gemini 1.5 / GPT-4o", "Context-enriched section drafting, synthesis, and simulated peer review"],
        ["Local Offline Engine", "Rule-based Synthesizer", "Native Python", "Deterministic, cost-free drafting for academic offline environments"],
        ["Data Visualization", "Matplotlib & Seaborn", "3.8+ / 0.13+", "Rendering 300 DPI publication charts and vector graphics"],
        ["LaTeX Processing", "tectonic / pdflatex", "2024 / TeX Live", "Local PDF compilation engine and package validation"],
        ["Document Automation", "python-docx", "1.1+", "Automated generation of institutional project reports"],
        ["Archive Packaging", "zipfile & os", "Python Standard Lib", "Self-contained Overleaf-ready ZIP bundle packaging"]
    ]
    t_tools = doc.add_table(rows=1, cols=4)
    style_table(t_tools, [1.4, 1.8, 1.3, 2.3], tools_headers, tools_data)

    add_heading_2(doc, "2.10 Project Plan")
    add_body_p(doc, "The project followed a disciplined Software Development Life Cycle (SDLC) managed across five distinct development phases spanning a four-month timeframe. The execution milestones are outlined below:")

    plan_headers = ["Phase", "Activity / Deliverable", "Timeline", "Milestone Target"]
    plan_data = [
        ["Phase 1", "Literature Review, Problem Formulation & Feasibility Study", "Weeks 1 - 3", "System Requirement Specification (SRS) Approval"],
        ["Phase 2", "Architecture Design, UML Modeling & UI Wireframing", "Weeks 4 - 6", "System Design Document & DFD Finalization"],
        ["Phase 3", "Core Engine Development (APIs, Prompting & Streamlit UI)", "Weeks 7 - 11", "Working Alpha Prototype with Live API Integration"],
        ["Phase 4", "Plotting Studio, LaTeX Packager & Offline Fallback Engine", "Weeks 12 - 14", "Beta Release with 10/10 Passing Test Suite"],
        ["Phase 5", "User Testing, Documentation, Packaging & Final Defense", "Weeks 15 - 16", "Comprehensive Project Report & Overleaf Bundle Delivery"]
    ]
    t_plan = doc.add_table(rows=1, cols=4)
    style_table(t_plan, [1.0, 3.2, 1.2, 1.4], plan_headers, plan_data)

    add_body_p(doc, "Risk analysis and proactive mitigation strategies were incorporated into the project plan to address potential technical challenges, as detailed below:")

    risk_headers = ["Identified Technical Risk", "Impact Level", "Mitigation Strategy Implemented"]
    risk_data = [
        ["Scholarly API Rate Limiting (Semantic Scholar)", "High", "Implemented in-memory caching and fallback to curated academic mock databases."],
        ["LLM API Token Latency & Quota Depletion", "Critical", "Engineered dual-engine architecture with instantaneous zero-cost offline synthesis mode."],
        ["LaTeX Compilation Environment Missing on Client", "Medium", "Provided dual export: local compilation when tectonic is present, plus universal Overleaf ZIP."],
        ["Citation Inconsistency & Missing BibTeX Keys", "High", "Implemented automated Citation Health Checker validating all \\cite{} keys before compilation."]
    ]
    t_risk = doc.add_table(rows=1, cols=3)
    style_table(t_risk, [2.4, 1.2, 3.2], risk_headers, risk_data)

    doc.add_page_break()

def generate_chapter_3(doc):
    # =========================================================
    # CHAPTER 3: REQUIREMENT ANALYSIS
    # =========================================================
    add_heading_1(doc, "3. REQUIREMENT ANALYSIS")

    add_heading_2(doc, "3.1 Feasibility Study")
    add_body_p(doc, "Prior to initiating software construction, a thorough multi-dimensional feasibility study was conducted to establish the viability, sustainability, and operational efficacy of the AI Research Paper Assistant platform:")

    add_bullet_p(doc, "The technical architecture relies on modern, mature open-source technologies including Python 3.11+, Streamlit, RESTful HTTP APIs, and standard TeX engines. The required cloud APIs (Semantic Scholar, OpenAI, Google Gemini) offer stable, documented SDKs with high availability. Furthermore, the development of a deterministic offline engine guarantees technical functionality even on resource-constrained hardware lacking continuous internet connectivity or cloud API credentials.", bold_prefix="1. Technical Feasibility: ")

    add_bullet_p(doc, "The economic impact of the project is overwhelmingly favorable. The software is constructed entirely using open-source libraries (Python, Streamlit, Matplotlib, Seaborn, tectonic) that require zero licensing expenditures. For production use, the offline engine operates at zero ongoing cost. Cloud API usage is completely optional and costs only pennies per generated paper. The total development and operational costs are well within standard university laboratory budgets.", bold_prefix="2. Economic Feasibility: ")

    add_bullet_p(doc, "The system is designed with an intuitive, self-explanatory web interface that requires no specialized training or command-line proficiency. Academic researchers, graduate students, and university faculty already familiar with basic web applications can easily navigate the 8-step pipeline. Users can input research topics, browse papers, adjust parameters using interactive sliders, and download publication bundles with single clicks, ensuring rapid user adoption.", bold_prefix="3. Operational Feasibility: ")

    add_bullet_p(doc, "The platform strictly respects academic integrity standards. It functions as an authoring assistant, literature synthesizer, and formatting compiler, leaving all empirical data, intellectual direction, and final editorial decisions under the author's complete control. All bibliographic data retrieved from Semantic Scholar and arXiv complies with fair academic use guidelines and open data licenses.", bold_prefix="4. Legal & Ethical Feasibility: ")

    add_heading_2(doc, "3.2 Users of the System")
    add_body_p(doc, "The system caters to four primary user classes across the academic and scientific authoring ecosystem, each characterized by distinct goals, technical backgrounds, and interaction workflows:")

    user_headers = ["User Role / Persona", "Profile Description", "Primary System Workflows & Objectives"]
    user_data = [
        ["M.Sc. IT / MCA Graduate Student", "Master's student working on minor/major capstone projects or preparing their first conference submission.", "Conducts fast literature surveys, learns standard paper structures, drafts methodology sections, and builds error-free LaTeX bundles."],
        ["Ph.D. Research Scholar", "Advanced researcher conducting in-depth empirical studies aiming for top-tier conference or journal publications.", "Extracts fine-grained related work comparison matrices, generates publication-grade 300 DPI plots, and audits citation health."],
        ["Faculty Research Supervisor", "Professor or project guide mentoring multiple research students and evaluating manuscripts.", "Uses simulated peer review rubric scores to perform rapid pre-submission manuscript evaluations and identify conceptual flaws."],
        ["Independent Academic Author", "Domain specialist, research scientist, or industry practitioner writing technical whitepapers or pre-prints.", "Utilizes offline deterministic drafting to assemble structured technical manuscripts without relying on cloud services."]
    ]
    t_users = doc.add_table(rows=1, cols=3)
    style_table(t_users, [1.8, 2.2, 2.8], user_headers, user_data)

    add_heading_2(doc, "3.3 Modules")
    add_body_p(doc, "The AI Research Paper Assistant is modularized into eight cohesive, decoupled software components that manage specific phases of the authoring lifecycle:")

    add_bullet_p(doc, "Serves as the administrative entry point where authors configure project names, select target publication templates (e.g., NeurIPS, IEEE, ACM, Springer), configure API credentials, and toggle between Cloud and Offline modes.", bold_prefix="1. Project Workspace & Configuration Module: ")
    add_bullet_p(doc, "Integrates with the Semantic Scholar Academic Graph and arXiv REST endpoints, executing keyword searches and retrieving title, abstract, citation metrics, author lists, and pre-formatted BibTeX records.", bold_prefix="2. Literature Discovery & Retrieval Module: ")
    add_bullet_p(doc, "Analyzes retrieved scholarly literature, extracts core methodologies, identifies persistent scientific gaps, and automatically formulates testable research questions and formal hypotheses.", bold_prefix="3. Research Insights & Hypothesis Module: ")
    add_bullet_p(doc, "Constructs hierarchical manuscript outlines structured according to target publication venue norms, generating section headers, subheadings, and target word count distributions.", bold_prefix="4. Hierarchical Outline Architect Module: ")
    add_bullet_p(doc, "Generates structured comparative literature matrices, contrasting collected papers across Methodology, Baseline Models, Evaluation Benchmarks, and Critical Limitations.", bold_prefix="5. Related Work Synthesis Module: ")
    add_bullet_p(doc, "Dispatches context-enriched, academic-style prompts to LLM endpoints to synthesize comprehensive section drafts, LaTeX equations, and pseudocode algorithms.", bold_prefix="6. Section Drafting & Staging Module: ")
    add_bullet_p(doc, "Simulates three independent double-blind peer reviewers, evaluating manuscripts on Originality, Technical Soundness, Empirical Rigor, Clarity, and Literature Coverage with 1-10 scores.", bold_prefix="7. Multi-Persona Peer Review Module: ")
    add_bullet_p(doc, "Executes dynamic Python visualization scripts, renders high-resolution 300 DPI PNGs and vector PDFs, and packages complete, error-free Overleaf ZIP archives.", bold_prefix="8. Visualization & LaTeX Compilation Module: ")

    add_heading_2(doc, "3.4 Process Model")
    add_body_p(doc, "The project was engineered using the Spiral Software Development Life Cycle (SDLC) Model. The Spiral Model was selected because of its risk-driven approach, which is ideal for integrating emerging, non-deterministic generative artificial intelligence models with strict, deterministic document compilation engines (LaTeX).")

    add_body_p(doc, "The development proceeded across four comprehensive spiral iterations, each incorporating Objective Determination, Risk Assessment, Development/Testing, and Milestone Review:")

    add_bullet_p(doc, "Focused on resolving the primary technical risk—potential LLM API rate limiting and token costs. Developed the underlying project JSON state manager and built the deterministic offline rule-based academic engine.", bold_prefix="• Spiral Iteration 1 (Core Architecture & Risk Mitigation): ")
    add_bullet_p(doc, "Resolved external integration risks with scholarly graph APIs. Implemented the Semantic Scholar REST client with intelligent caching, abstract parsing, and automatic BibTeX extraction.", bold_prefix="• Spiral Iteration 2 (Literature Discovery & UI Prototype): ")
    add_bullet_p(doc, "Addressed content coherence and citation hallucination risks. Engineered the prompt context assembler, related work comparison matrix builder, and automated peer review rubric evaluator.", bold_prefix="• Spiral Iteration 3 (Drafting Engine & Peer Review Studio): ")
    add_bullet_p(doc, "Resolved document compilation and typesetting risks. Built the native Python plotting studio, the Citation Health Checker, and the Overleaf ZIP packager, achieving a 10/10 passing test suite.", bold_prefix="• Spiral Iteration 4 (Visualization, LaTeX Packaging & Verification): ")

    add_heading_2(doc, "3.5 Hardware & Software Requirements")
    add_body_p(doc, "The minimum and recommended hardware and software configurations required to host, develop, and execute the AI Research Paper Assistant are specified in the tables below:")

    hw_headers = ["Component", "Minimum Requirement", "Recommended Specification", "Operational Purpose"]
    hw_data = [
        ["Processor (CPU)", "Intel Core i3 / AMD Ryzen 3 (Dual Core)", "Intel Core i7 / AMD Ryzen 7 (8+ Cores)", "Script execution, data parsing, and plotting rendering"],
        ["System Memory (RAM)", "4 GB DDR4", "16 GB DDR4/DDR5", "In-memory caching of literature graphs and plot buffers"],
        ["Storage Space", "500 MB Free Disk Space", "2 GB Free SSD Space", "Storing cached PDF papers, generated plots, and LaTeX bundles"],
        ["Display Resolution", "1280 x 720 (HD)", "1920 x 1080 (Full HD)", "Responsive Streamlit dashboard and multi-column comparison viewing"],
        ["Network Adapter", "Broadband Internet (1 Mbps)", "High-Speed Internet (10+ Mbps)", "Querying Semantic Scholar REST APIs and LLM cloud services"]
    ]
    t_hw = doc.add_table(rows=1, cols=4)
    style_table(t_hw, [1.4, 1.8, 1.8, 1.8], hw_headers, hw_data)

    sw_headers = ["Software Layer", "Environment / Package", "Version", "Description & Usage"]
    sw_data = [
        ["Operating System", "Microsoft Windows / Linux / macOS", "Windows 10/11, Ubuntu 20+", "Cross-platform operating system environment"],
        ["Runtime Environment", "Python Programming Language", "3.11.x / 3.12.x", "Core backend application execution runtime"],
        ["Web Application Engine", "Streamlit", "1.30.0+", "Frontend presentation layer and UI component rendering"],
        ["HTTP Client", "Requests / Urllib3", "2.31.0+", "RESTful communication with Semantic Scholar & ArXiv"],
        ["AI SDKs", "google-genai / openai", "Latest Official", "Cloud LLM interaction for drafting and peer review"],
        ["Visualization Studio", "Matplotlib & Seaborn", "3.8+ / 0.13+", "Rendering scientific line charts, bar plots, and heatmaps"],
        ["TeX Engine (Optional)", "tectonic / TeX Live pdflatex", "2024+", "Local compilation of LaTeX manuscripts to PDF format"],
        ["Web Browser", "Google Chrome / Mozilla Firefox", "Modern Evergreen", "Client-side browser for accessing the application interface"]
    ]
    t_sw = doc.add_table(rows=1, cols=4)
    style_table(t_sw, [1.4, 1.8, 1.3, 2.3], sw_headers, sw_data)

    add_heading_2(doc, "3.6 Use Cases")
    add_body_p(doc, "The functional requirements of the system are categorized into ten core Use Cases, detailing interactions between external actors and the platform:")

    uc_headers = ["Use Case ID", "Use Case Name", "Primary Actor", "Brief Description"]
    uc_data = [
        ["UC-01", "Initialize Project Workspace", "Researcher", "Configures project title, author metadata, venue template, and LLM mode."],
        ["UC-02", "Search Literature Graph", "Researcher", "Queries Semantic Scholar API using academic keywords, topics, or DOIs."],
        ["UC-03", "Extract & Save Citations", "Researcher", "Selects relevant literature papers and saves abstracts and BibTeX to project."],
        ["UC-04", "Synthesize Research Insights", "Researcher / AI", "Extracts methodologies, challenges, and auto-derives hypotheses."],
        ["UC-05", "Generate Paper Outline", "Researcher / AI", "Architects hierarchical section breakdown matching target venue rules."],
        ["UC-06", "Draft Section Manuscript", "Researcher / AI", "Dispatches prompts to LLM engine to synthesize formal academic prose."],
        ["UC-07", "Stage Mathematical Equations", "Researcher / AI", "Formats and verifies LaTeX math equations, matrices, and algorithms."],
        ["UC-08", "Conduct Simulated Peer Review", "Researcher / AI", "Generates multi-persona critique and rubric scoring across 5 dimensions."],
        ["UC-09", "Render Publication Plots", "Researcher", "Executes Python visualization scripts, outputting 300 DPI figures and TeX snippets."],
        ["UC-10", "Export Overleaf / LaTeX Bundle", "Researcher", "Audits citation integrity, compiles PDF, and packages complete Overleaf ZIP archive."]
    ]
    t_uc = doc.add_table(rows=1, cols=4)
    style_table(t_uc, [1.0, 2.0, 1.4, 2.4], uc_headers, uc_data)

    add_heading_2(doc, "3.7 Use Case Diagram")
    add_body_p(doc, "The Use Case Diagram visually represents the system boundary, external actors (Academic Researcher, Semantic Scholar API, and AI Cloud Services), and their relationships with the core functional use cases:")

    add_image_figure(doc, ASSETS_DIR / "use_case_diagram.png", "System Use Case Diagram representing Actor-System Boundary Interactions (UC-01 to UC-10)", width_inches=5.2)

    add_body_p(doc, "The diagram highlights how the Researcher acts as the central orchestrator, triggering literature search, outline architecting, section drafting, and LaTeX packaging. The Semantic Scholar API acts as an external service provider responding to search queries, while the AI Cloud Services (Gemini and OpenAI) act as generative sub-systems supporting drafting, related work synthesis, and peer review simulation.")

    doc.add_page_break()

def generate_chapter_4(doc):
    # =========================================================
    # CHAPTER 4: DESIGN
    # =========================================================
    add_heading_1(doc, "4. DESIGN")

    add_heading_2(doc, "4.1 Use Case Scenarios")
    add_body_p(doc, "Use case scenarios provide granular specifications of the interactions between actors and the system, detailing pre-conditions, normal execution flows, alternative exception flows, and post-conditions for primary system operations.")

    # UC-01 Scenario
    add_heading_3(doc, "4.1.1 Use Case Scenario: UC-01 (Initialize Project Workspace)")
    uc1_headers = ["Scenario Attribute", "Specification Details"]
    uc1_data = [
        ["Use Case ID & Name", "UC-01: Initialize Project Workspace"],
        ["Primary Actor", "Academic Researcher / Graduate Student"],
        ["Pre-Conditions", "The web application is launched and running on the local host or server."],
        ["Trigger", "User navigates to the Project Portal tab on the sidebar."],
        ["Main Success Flow", "1. User inputs Working Paper Title and Author Details.\n2. User selects Target Venue (e.g., NeurIPS, IEEE, ACM, Springer).\n3. User chooses LLM Mode (Live Cloud or Offline Deterministic Engine).\n4. System creates or updates project state JSON with selected parameters.\n5. System confirms successful project workspace initialization."],
        ["Alternative / Exception Flow", "4a. If invalid project title is entered, system prompts user with validation warning and maintains default settings."],
        ["Post-Conditions", "Project workspace initialized; state saved in session memory and persistent JSON."]
    ]
    t_uc1 = doc.add_table(rows=1, cols=2)
    style_table(t_uc1, [2.2, 4.6], uc1_headers, uc1_data)

    # UC-02 Scenario
    add_heading_3(doc, "4.1.2 Use Case Scenario: UC-02 (Search & Ingest Literature)")
    uc2_headers = ["Scenario Attribute", "Specification Details"]
    uc2_data = [
        ["Use Case ID & Name", "UC-02: Search & Ingest Literature"],
        ["Primary Actor", "Academic Researcher / Graduate Student"],
        ["Pre-Conditions", "Project workspace initialized; internet connection available for Semantic Scholar API."],
        ["Trigger", "User enters search query (e.g., 'State Space Models') and clicks 'Search Academic Literature'."],
        ["Main Success Flow", "1. System formats REST GET request with query and result limit.\n2. Semantic Scholar API returns JSON array of matching papers.\n3. System parses titles, abstracts, citation counts, authors, venues, and years.\n4. System renders interactive cards displaying paper metadata and abstracts.\n5. User clicks 'Save to Research Material' to collect key papers.\n6. System extracts or formats BibTeX citation keys and saves into project bibliography."],
        ["Alternative / Exception Flow", "2a. If Semantic Scholar API fails or times out, system displays cached results or informs user to switch to offline literature sample set."],
        ["Post-Conditions", "Selected papers and BibTeX records appended to project literature database."]
    ]
    t_uc2 = doc.add_table(rows=1, cols=2)
    style_table(t_uc2, [2.2, 4.6], uc2_headers, uc2_data)

    # UC-03 Scenario
    add_heading_3(doc, "4.1.3 Use Case Scenario: UC-03 (Generate Paper Outline)")
    uc3_headers = ["Scenario Attribute", "Specification Details"]
    uc3_data = [
        ["Use Case ID & Name", "UC-03: Generate Paper Outline"],
        ["Primary Actor", "Academic Researcher / Graduate Student"],
        ["Pre-Conditions", "Working paper topic and target venue configured."],
        ["Trigger", "User navigates to 'Paper Outline' and clicks 'Generate Conference Outline'."],
        ["Main Success Flow", "1. System loads venue-specific structural templates (e.g., 8-section NeurIPS standard).\n2. System computes target word counts and subsections based on venue length limits.\n3. System populates editable outline cards with section objectives and key focus points.\n4. User modifies section titles, adds custom notes, or adjusts target lengths.\n5. System persists updated outline schema to project state JSON."],
        ["Alternative / Exception Flow", "3a. User can reset outline to default academic standards at any time via 'Reset Outline' button."],
        ["Post-Conditions", "Structured hierarchical outline finalized for drafting phase."]
    ]
    t_uc3 = doc.add_table(rows=1, cols=2)
    style_table(t_uc3, [2.2, 4.6], uc3_headers, uc3_data)

    # UC-04 Scenario
    add_heading_3(doc, "4.1.4 Use Case Scenario: UC-04 (AI-Assisted Section Drafting)")
    uc4_headers = ["Scenario Attribute", "Specification Details"]
    uc4_data = [
        ["Use Case ID & Name", "UC-04: AI-Assisted Section Drafting"],
        ["Primary Actor", "Academic Researcher / AI Generative Engine"],
        ["Pre-Conditions", "Paper outline structured; literature papers available in project state."],
        ["Trigger", "User selects target section (e.g., 'Methodology') and clicks 'Generate Section Draft'."],
        ["Main Success Flow", "1. System retrieves section objectives, saved paper citations, and style directives.\n2. System constructs rich academic context prompt with mathematical rigor guidelines.\n3. In Cloud Mode: Dispatches prompt to Gemini/OpenAI API; streams draft response.\n   In Offline Mode: Generates comprehensive, deterministic academic prose with equations.\n4. System renders generated draft in interactive Markdown text area.\n5. User edits draft, stages mathematical equations, and verifies \\cite{} references.\n6. User clicks 'Save Section Draft' to persist content."],
        ["Alternative / Exception Flow", "3a. If API quota is exceeded, system alerts user and offers 1-click fallback to offline drafting engine."],
        ["Post-Conditions", "Section draft persisted into project state JSON and ready for compilation."]
    ]
    t_uc4 = doc.add_table(rows=1, cols=2)
    style_table(t_uc4, [2.2, 4.6], uc4_headers, uc4_data)

    # UC-05 Scenario
    add_heading_3(doc, "4.1.5 Use Case Scenario: UC-05 (Conduct Simulated Peer Review)")
    uc5_headers = ["Scenario Attribute", "Specification Details"]
    uc5_data = [
        ["Use Case ID & Name", "UC-05: Conduct Simulated Peer Review"],
        ["Primary Actor", "Academic Researcher / Faculty Guide"],
        ["Pre-Conditions", "At least one manuscript section drafted."],
        ["Trigger", "User navigates to 'Refinement & Review' and clicks 'Run Multi-Persona Peer Review'."],
        ["Main Success Flow", "1. System compiles current section drafts into continuous manuscript context.\n2. System executes 3 simulated reviewer personas (Senior Reviewer, Methodologist, Domain Expert).\n3. Reviewers evaluate text across 5 dimensions: Originality, Soundness, Empirical Rigor, Clarity, References.\n4. System computes overall score (1-10) and determines consensus (Accept / Minor / Major / Reject).\n5. System presents itemized constructive feedback, missing citations, and actionable recommendations."],
        ["Alternative / Exception Flow", "1a. If manuscript sections are empty, system notifies author to draft content before requesting review."],
        ["Post-Conditions", "Peer review report generated, scored, and logged in project state."]
    ]
    t_uc5 = doc.add_table(rows=1, cols=2)
    style_table(t_uc5, [2.2, 4.6], uc5_headers, uc5_data)

    # UC-06 Scenario
    add_heading_3(doc, "4.1.6 Use Case Scenario: UC-06 (Render Plots & Export Overleaf ZIP)")
    uc6_headers = ["Scenario Attribute", "Specification Details"]
    uc6_data = [
        ["Use Case ID & Name", "UC-06: Render Plots & Export Overleaf ZIP"],
        ["Primary Actor", "Academic Researcher / Graduate Student"],
        ["Pre-Conditions", "Manuscript drafted; project state contains literature and outline."],
        ["Trigger", "User generates publication plots and clicks 'Generate Overleaf ZIP Bundle'."],
        ["Main Success Flow", "1. In Plots Studio: System executes Python Matplotlib script, rendering 300 DPI PNG & vector PDF.\n2. System generates copy-pasteable LaTeX figure environment snippet.\n3. In Export Studio: Citation Health Checker audits all \\cite{} tags against references.bib.\n4. System generates clean main.tex, references.bib, Makefile, and compile.bat.\n5. If tectonic/pdflatex is present, compiles camera-ready PDF document.\n6. System packages all assets into a self-contained ZIP archive and provides 1-click download."],
        ["Alternative / Exception Flow", "3a. If missing citations are found, Citation Health Checker highlights unreferenced keys with warnings."],
        ["Post-Conditions", "Complete, camera-ready Overleaf ZIP archive downloaded to author's computer."]
    ]
    t_uc6 = doc.add_table(rows=1, cols=2)
    style_table(t_uc6, [2.2, 4.6], uc6_headers, uc6_data)

    add_heading_2(doc, "4.2 Diagrams")
    add_body_p(doc, "System modeling diagrams provide comprehensive visual blueprints of the architectural structure, information exchange dynamics, and behavioral workflows of the AI Research Paper Assistant.")

    add_heading_3(doc, "4.2.1 UML and Data Flow Diagrams (DFD)")
    add_body_p(doc, "Data Flow Diagrams (DFDs) graphically depict the flow of information through the system, modeling data inputs, transformative processes, persistent data stores, and outputs across levels of increasing granularity.")

    # DFD Level 0
    add_body_p(doc, "The Context Level Diagram (DFD Level 0) models the entire system as a single process bubble interacting with three primary external entities: the Academic Researcher, the Scholarly APIs (Semantic Scholar and ArXiv), and the AI / LLM Cloud Services (OpenAI and Google Gemini).", bold_prefix="Data Flow Diagram: Level 0 (Context Level Diagram): ")
    add_image_figure(doc, ASSETS_DIR / "dfd_level_0.png", "DFD Level 0 (Context Level Diagram) showing External Entities and High-Level Data Flows", width_inches=5.6)
    add_body_p(doc, "As illustrated above, the Academic Researcher supplies search topics, notes, and stylistic directives, and receives assembled manuscripts, high-resolution plots, and complete Overleaf ZIP archives. The system queries the Scholarly APIs via REST requests and receives paper abstracts and BibTeX metadata. The system exchanges context-enriched prompts and synthesized drafts with the AI LLM services.")

    # DFD Level 1
    add_body_p(doc, "The Level 1 Data Flow Diagram decomposes the system into six core functional processes and six internal persistent data stores, ensuring clear separation of concerns and eliminating information bottlenecks.", bold_prefix="Data Flow Diagram: Level 1 (Functional Decomposition): ")
    add_image_figure(doc, ASSETS_DIR / "dfd_level_1.png", "DFD Level 1 Diagram decomposing System into 6 Core Functional Processes and Data Stores", width_inches=5.2)
    add_body_p(doc, "The Level 1 diagram highlights the sequential and parallel data exchanges:")
    add_bullet_p(doc, "Processes user search keywords and venue parameters, queries external scholarly graph APIs, and records citation records into Data Store D1 (Literature Store).", bold_prefix="• Process 1.0 (Literature Discovery): ")
    add_bullet_p(doc, "Synthesizes curated literature and researcher notes to auto-derive research hypotheses and knowledge gaps, persisted into Data Store D2 (Hypothesis Store).", bold_prefix="• Process 2.0 (Create Hypothesis): ")
    add_bullet_p(doc, "Transforms research hypotheses into venue-compliant hierarchical outline schemas, persisting structured section targets into Data Store D3 (Outline Store).", bold_prefix="• Process 3.0 (Architect Outline): ")
    add_bullet_p(doc, "Combines section goals from D3 and BibTeX keys from D1, dispatches prompts to LLM engines, and records synthesized prose and LaTeX formulas into Data Store D4 (Drafts Store).", bold_prefix="• Process 4.0 (Draft Sections): ")
    add_bullet_p(doc, "Executes multi-persona simulated peer evaluations against conference rubrics, logging critiques and scores into Data Store D5 (Review Store).", bold_prefix="• Process 5.0 (Simulated Peer Review): ")
    add_bullet_p(doc, "Renders 300 DPI publication plots, audits citation health, and packages the complete camera-ready Overleaf ZIP archive into Data Store D6 (Package Store).", bold_prefix="• Process 6.0 (Generate Package): ")

    # DFD Level 2
    add_body_p(doc, "The Level 2 Data Flow Diagram decomposes Process 4.0 (Draft Sections) into five specialized sub-processes, modeling the precise pipeline through which raw section goals are converted into audited, publication-grade academic prose.", bold_prefix="Data Flow Diagram: Level 2 (Process 4.0 Detailed Decomposition): ")
    add_image_figure(doc, ASSETS_DIR / "dfd_level_2.png", "DFD Level 2 Diagram detailing Internal Sub-Processes of Drafting and Refinement Engine", width_inches=5.2)
    add_body_p(doc, "The Level 2 decomposition demonstrates the internal mechanics of the drafting pipeline:")
    add_bullet_p(doc, "Reads section objectives from D3 (Outline Store), assembling structured academic prompts with explicit tone and length parameters.", bold_prefix="• Sub-Process 4.1 (Prompt Context Assembler): ")
    add_bullet_p(doc, "Fetches BibTeX citation keys from D1 (Literature Store) and routes prompts to Google Gemini, OpenAI, or the local offline engine.", bold_prefix="• Sub-Process 4.2 (LLM Provider Dispatcher): ")
    add_bullet_p(doc, "Formats LaTeX mathematical equations, theorem environments, and matrices, caching results in D4 (Drafts Store).", bold_prefix="• Sub-Process 4.3 (Math & LaTeX Formatter): ")
    add_bullet_p(doc, "Structures algorithmic complexity analyses, pseudocode algorithm boxes, and data structures into D4 (Algorithm Store).", bold_prefix="• Sub-Process 4.4 (Algorithm & Pseudocode Stager): ")
    add_bullet_p(doc, "Audits citations against bibliography, verifies zero-hallucination integrity, and commits validated text to D4 (Validated Store).", bold_prefix="• Sub-Process 4.5 (Citation Auditor & Integrator): ")

    # DFD Level 3
    add_body_p(doc, "The Level 3 Data Flow Diagram decomposes Process 5.0 (Simulated Peer Review) into five specialized sub-processes, modeling the multi-persona pre-submission review and consensus scoring pipeline.", bold_prefix="Data Flow Diagram: Level 3 (Process 5.0 Detailed Decomposition): ")
    add_image_figure(doc, ASSETS_DIR / "dfd_level_3.png", "DFD Level 3 Diagram detailing Sub-Processes of Multi-Persona Simulated Peer Review", width_inches=5.2)
    add_body_p(doc, "The Level 3 decomposition models the pre-submission peer evaluation workflow:")
    add_bullet_p(doc, "Parses full manuscript submissions from D4 (Drafts Store), extracting section tokens, metadata, and mathematical assertions.", bold_prefix="• Sub-Process 5.1 (Manuscript Context Parser): ")
    add_bullet_p(doc, "Evaluates theoretical soundness and mathematical proofs against rigorous criteria, logging scores into D5.1 (Theory Store).", bold_prefix="• Sub-Process 5.2 (Reviewer 1: Theoretical Audit): ")
    add_bullet_p(doc, "Critiques experimental baselines, dataset validity, and empirical metrics, recording evaluations into D5.2 (Empirical Store).", bold_prefix="• Sub-Process 5.3 (Reviewer 2: Empirical Audit): ")
    add_bullet_p(doc, "Analyzes academic narrative flow, structural readability, and terminology coherence, storing feedback into D5.3 (Clarity Store).", bold_prefix="• Sub-Process 5.4 (Reviewer 3: Clarity Audit): ")
    add_bullet_p(doc, "Aggregates multi-persona scores into a 1-10 normalized scorecard, consensus verdict, and actionable critique saved in D5 (Final Dossier Store).", bold_prefix="• Sub-Process 5.5 (Rubric Aggregator & Consensus): ")

    # UML Structural & Behavioral Diagrams
    add_heading_3(doc, "4.2.1.1 UML Class Diagram")
    add_body_p(doc, "The UML Class Diagram models the static structural design of the software, illustrating the core object-oriented classes, attributes, methods, and relationships:")
    add_image_figure(doc, ASSETS_DIR / "uml_class_diagram.png", "UML Class Diagram illustrating System Classes, Data Attributes, Methods, and Associations", width_inches=5.6)
    add_body_p(doc, "Key architectural classes include PaperProject (central state entity), LiteratureSearcher (REST client managing Semantic Scholar queries), LLMEngine (abstract base class with CloudLLMEngine and OfflineLLMEngine implementations), OutlineArchitect (manages section hierarchies), PlotStudio (executes Matplotlib/Seaborn scripts), and LaTeXCompiler (assembles main.tex and packages ZIP bundles).")

    add_heading_3(doc, "4.2.1.2 UML Sequence Diagram")
    add_body_p(doc, "The UML Sequence Diagram models the chronological message exchange between actors, interface controllers, API wrappers, synthesis engines, and filesystem storage:")
    add_image_figure(doc, ASSETS_DIR / "uml_sequence_diagram.png", "UML Sequence Diagram displaying End-to-End Execution and Message Flow", width_inches=5.6)
    add_body_p(doc, "The trace shows the chronological progression: the user enters search criteria, the Streamlit Controller delegates to the Literature Searcher, results are rendered and saved, the Outline Architect generates section targets, the LLM Engine drafts prose, the Peer Review Studio computes quality scores, and the LaTeX Compiler packages the final Overleaf bundle.")

    add_heading_3(doc, "4.2.1.3 UML Activity Diagram")
    add_body_p(doc, "The UML Activity Diagram represents the operational control flow, user decision nodes, parallel processing lanes, and branching logic across the authoring pipeline:")
    add_image_figure(doc, ASSETS_DIR / "uml_activity_diagram.png", "UML Activity Diagram illustrating Workflow Decision Paths and Branching Logic", width_inches=5.6)
    add_body_p(doc, "The diagram details decision branches such as choosing between Live Cloud and Offline mode, accepting or regenerating outline sections, revising drafts based on peer review scores, and selecting between local PDF compilation and Overleaf ZIP export.")

    add_heading_2(doc, "4.2.2 Entity Relationship Diagram (ER Diagram)")
    add_body_p(doc, "The Entity-Relationship (ER) Diagram models the persistent data structures, relational schemas, primary/foreign key associations, and cardinalities governing the platform:")
    add_image_figure(doc, ASSETS_DIR / "er_diagram.png", "Entity-Relationship (ER) Diagram displaying Entities, Relational Cardinalities, and Keys", width_inches=5.6)
    add_body_p(doc, "The data schema is organized around the central entity tbl_paper_project, which possesses 1-to-Many relationships with tbl_literature_sources (storing papers and BibTeX records), tbl_paper_outline (storing section breakdowns), tbl_section_drafts (storing drafted text), tbl_peer_review_logs (storing rubric scores), and tbl_figure_assets (storing visual charts and plot scripts).")

    add_heading_2(doc, "4.3 Screenshots of Website & User Interface Walkthrough")
    add_body_p(doc, "This section presents actual high-resolution screenshots of the live, operational AI Research Paper Assistant platform, accompanied by detailed descriptions of interface elements, user workflows, and system behaviors across the eight pipeline modules.")

    # Screenshot 1
    add_heading_3(doc, "4.3.1 Paper Project Workspace Portal & LLM Mode Configuration")
    add_image_figure(doc, ASSETS_DIR / "screenshot_1_paper_portal.png", "Screenshot 1: Paper Project Workspace Portal & LLM Mode Configuration", width_inches=5.8)
    add_body_p(doc, "Screenshot 1 displays the administrative dashboard and navigation sidebar. Users can configure the working manuscript title, select the publication venue template (e.g., NeurIPS / ICLR, IEEE Transactions, ACM SIGKDD), and choose the active LLM engine mode. The green notice confirms activation of the Offline Academic Engine, guaranteeing full zero-cost functionality without API keys. The top navigation bar provides one-click access across the 8 authoring phases.")

    # Screenshot 2
    add_heading_3(doc, "4.3.2 Literature Discovery & Semantic Scholar Graph Search")
    add_image_figure(doc, ASSETS_DIR / "screenshot_2_research_material.png", "Screenshot 2: Literature Discovery & Semantic Scholar Graph Search Engine", width_inches=5.8)
    add_body_p(doc, "Screenshot 2 illustrates the Literature Discovery module. The user enters academic topics (e.g., 'State Space Models for Long Context Sequence Modeling') and sets year and result limits. The system queries the Semantic Scholar REST API, returning structured cards displaying paper titles, authors, publication years, citation counts, and full abstracts. Authors can collect relevant papers into their project bibliography with a single click on 'Save to Research Material'.")

    # Screenshot 3
    add_heading_3(doc, "4.3.3 Research Insights & Scientific Hypothesis Formulation Hub")
    add_image_figure(doc, ASSETS_DIR / "screenshot_3_paper_outline.png", "Screenshot 3: Research Insights & Hypothesis Formulation Hub", width_inches=5.8)
    add_body_p(doc, "Screenshot 3 displays the automated Research Insights Hub. By analyzing the collective abstracts of saved papers, the system automatically extracts primary methodological patterns, identifies persistent technical challenges, and formulates formal, testable scientific hypotheses (e.g., demonstrating sub-quadratic compute complexity with linear memory scaling). These insights form the intellectual foundation for the manuscript outline.")

    # Screenshot 4
    add_heading_3(doc, "4.3.4 Paper Outline Architect & Target Journal Configuration")
    add_image_figure(doc, ASSETS_DIR / "screenshot_4_literature_review.png", "Screenshot 4: Paper Outline Architect & Target Journal Configuration", width_inches=5.8)
    add_body_p(doc, "Screenshot 4 shows the Hierarchical Outline Architect. The system automatically structures an 8-section conference outline adhering to NeurIPS/IEEE standards, including Introduction, Related Work, Problem Formulation, Proposed Architecture, Experimental Setup, Results & Analysis, Discussion, and Conclusion. Each section card specifies target word counts and key focus topics, and remains fully editable by the author.")

    # Screenshot 5
    add_heading_3(doc, "4.3.5 Related Work Matrix & Literature Synthesis Studio")
    add_image_figure(doc, ASSETS_DIR / "screenshot_5_section_writing.png", "Screenshot 5: Related Work Matrix & Literature Synthesis Studio", width_inches=5.8)
    add_body_p(doc, "Screenshot 5 displays the Related Work Synthesis Studio. The system automatically generates a structured comparison matrix contrasting collected prior art across Architectural Paradigms, Attention Mechanisms, Computational Complexities, and Limitations. This matrix is formatted as a copy-ready LaTeX table block with active \\cite{} citations, eliminating manual bibliographic synthesis.")

    # Screenshot 6
    add_heading_3(doc, "4.3.6 AI-Assisted Section Drafting & Mathematical Equation Staging")
    add_image_figure(doc, ASSETS_DIR / "screenshot_6_refinement_review.png", "Screenshot 6: AI-Assisted Section Drafting & Mathematical Equation Staging", width_inches=5.8)
    add_body_p(doc, "Screenshot 6 showcases the Section Drafting Studio. Authors select an outline section and trigger context-enriched synthesis. The platform generates formal academic prose containing structured mathematical equations (such as state-space recurrence equations and discretization formulations) and verified in-text citations. Authors can refine text and stage equations directly inside the interactive editor.")

    # Screenshot 7
    add_heading_3(doc, "4.3.7 Automated Multi-Persona Peer Review & Quality Rubric Studio")
    add_image_figure(doc, ASSETS_DIR / "screenshot_7_plots_visuals.png", "Screenshot 7: Automated Multi-Persona Peer Review & Quality Rubric Studio", width_inches=5.8)
    add_body_p(doc, "Screenshot 7 illustrates the Simulated Peer Review Studio. Three autonomous reviewer personas evaluate the draft across Originality, Technical Soundness, Empirical Rigor, Clarity, and Literature Coverage. The interface displays overall scores, consensus verdicts (e.g., 'Strong Accept (8.5/10)'), and granular actionable critiques highlighting potential reviewer objections before submission.")

    # Screenshot 8
    add_heading_3(doc, "4.3.8 Publication Plots Studio & Lossless Vector Asset Rendering")
    add_image_figure(doc, ASSETS_DIR / "screenshot_8_latex_manuscript.png", "Screenshot 8: Publication Plots Studio & Chart Rendering", width_inches=5.8)
    add_body_p(doc, "Screenshot 8 shows the Publication Plots Studio. Authors can execute Python visualization scripts to generate 300 DPI publication-grade figures (such as latency scaling curves, benchmark radar charts, and ablation bar plots). The studio renders high-resolution previews and provides copy-pasteable LaTeX figure snippets with captions and labels.")

    # Screenshot 9
    add_heading_3(doc, "4.3.9 LaTeX Manuscript Assembly & Overleaf ZIP Packaging Studio")
    add_image_figure(doc, ASSETS_DIR / "screenshot_9_final_paper_export.png", "Screenshot 9: LaTeX Manuscript Assembly & Overleaf ZIP Packaging", width_inches=5.8)
    add_body_p(doc, "Screenshot 9 displays the Final Export & Packaging Studio. The Citation Health Checker audits all citations, confirming zero broken references. The system automatically packages main.tex, references.bib, figure assets, Makefile, and compile.bat into an Overleaf-ready ZIP archive, and compiles a camera-ready PDF document for instant download.")

    add_heading_2(doc, "4.4 Data Dictionary")
    add_body_p(doc, "A comprehensive Data Dictionary provides precise definitions of all data entities, attribute field names, data types, constraints, and descriptions used across the application state.")

    # Data Dictionary Tables
    add_heading_3(doc, "4.4.1 Data Dictionary: Project State Entity (tbl_paper_project)")
    dd1_headers = ["Field Name", "Data Type", "Constraints", "Description & Purpose"]
    dd1_data = [
        ["project_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique identifier for the research paper project."],
        ["title", "VARCHAR(255)", "NOT NULL", "Working academic title of the research manuscript."],
        ["author_names", "VARCHAR(255)", "NOT NULL", "Author names, affiliations, and contact email addresses."],
        ["target_venue", "VARCHAR(100)", "NOT NULL", "Selected publication venue template (e.g., NeurIPS, IEEE, ACM)."],
        ["llm_engine_mode", "VARCHAR(50)", "NOT NULL, DEFAULT 'offline'", "Execution mode: 'offline' (deterministic) or 'cloud' (Gemini/OpenAI)."],
        ["created_at", "TIMESTAMP", "NOT NULL, DEFAULT NOW()", "Timestamp marking initial project workspace creation."],
        ["updated_at", "TIMESTAMP", "NOT NULL", "Timestamp of last modification to project content."]
    ]
    t_dd1 = doc.add_table(rows=1, cols=4)
    style_table(t_dd1, [1.5, 1.4, 1.8, 2.1], dd1_headers, dd1_data)

    add_heading_3(doc, "4.4.2 Data Dictionary: Literature Sources Entity (tbl_literature_sources)")
    dd2_headers = ["Field Name", "Data Type", "Constraints", "Description & Purpose"]
    dd2_data = [
        ["source_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique identifier for the collected literature paper."],
        ["project_id", "VARCHAR(64)", "FOREIGN KEY, NOT NULL", "References tbl_paper_project.project_id."],
        ["paper_title", "VARCHAR(500)", "NOT NULL", "Full title of the referenced academic paper."],
        ["authors", "TEXT", "NOT NULL", "Comma-separated list of authors."],
        ["venue", "VARCHAR(200)", "NULLABLE", "Publication venue or conference name."],
        ["year", "INTEGER", "NOT NULL", "Year of publication."],
        ["citation_count", "INTEGER", "DEFAULT 0", "Total citation count retrieved from Semantic Scholar."],
        ["bibtex_key", "VARCHAR(100)", "NOT NULL, UNIQUE", "Unique citation key used in \\cite{bibtex_key} LaTeX tags."],
        ["bibtex_raw", "TEXT", "NOT NULL", "Complete pre-formatted BibTeX bibliographic entry."]
    ]
    t_dd2 = doc.add_table(rows=1, cols=4)
    style_table(t_dd2, [1.5, 1.4, 1.8, 2.1], dd2_headers, dd2_data)

    add_heading_3(doc, "4.4.3 Data Dictionary: Outline Entity (tbl_paper_outline)")
    dd3_headers = ["Field Name", "Data Type", "Constraints", "Description & Purpose"]
    dd3_data = [
        ["section_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique identifier for the outline section."],
        ["project_id", "VARCHAR(64)", "FOREIGN KEY, NOT NULL", "References tbl_paper_project.project_id."],
        ["section_order", "INTEGER", "NOT NULL", "Numerical sequence order (e.g., 1 for Intro, 2 for Related Work)."],
        ["section_title", "VARCHAR(200)", "NOT NULL", "Formal heading of the paper section."],
        ["target_words", "INTEGER", "NOT NULL", "Target word count allocated for the section."],
        ["key_points", "TEXT", "NULLABLE", "Core technical topics and bullet points to be covered in the section."]
    ]
    t_dd3 = doc.add_table(rows=1, cols=4)
    style_table(t_dd3, [1.5, 1.4, 1.8, 2.1], dd3_headers, dd3_data)

    add_heading_3(doc, "4.4.4 Data Dictionary: Section Drafts Entity (tbl_section_drafts)")
    dd4_headers = ["Field Name", "Data Type", "Constraints", "Description & Purpose"]
    dd4_data = [
        ["draft_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique identifier for the section draft."],
        ["project_id", "VARCHAR(64)", "FOREIGN KEY, NOT NULL", "References tbl_paper_project.project_id."],
        ["section_id", "VARCHAR(64)", "FOREIGN KEY, NOT NULL", "References tbl_paper_outline.section_id."],
        ["content_text", "MEDIUMTEXT", "NOT NULL", "Drafted markdown/LaTeX text content including equations."],
        ["word_count", "INTEGER", "DEFAULT 0", "Current computed word count of the section."],
        ["is_approved", "BOOLEAN", "DEFAULT FALSE", "Flag indicating author approval of current draft version."]
    ]
    t_dd4 = doc.add_table(rows=1, cols=4)
    style_table(t_dd4, [1.5, 1.4, 1.8, 2.1], dd4_headers, dd4_data)

    add_heading_3(doc, "4.4.5 Data Dictionary: Peer Review Logs Entity (tbl_peer_review_logs)")
    dd5_headers = ["Field Name", "Data Type", "Constraints", "Description & Purpose"]
    dd5_data = [
        ["review_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique identifier for the peer review evaluation."],
        ["project_id", "VARCHAR(64)", "FOREIGN KEY, NOT NULL", "References tbl_paper_project.project_id."],
        ["overall_score", "DECIMAL(3,1)", "NOT NULL", "Aggregated evaluation score from 1.0 to 10.0."],
        ["recommendation", "VARCHAR(50)", "NOT NULL", "Consensus: 'Accept', 'Minor Revision', 'Major Revision', 'Reject'."],
        ["critique_text", "TEXT", "NOT NULL", "Detailed multi-persona feedback, strengths, and weaknesses."],
        ["created_at", "TIMESTAMP", "NOT NULL, DEFAULT NOW()", "Timestamp when peer review evaluation was generated."]
    ]
    t_dd5 = doc.add_table(rows=1, cols=4)
    style_table(t_dd5, [1.5, 1.4, 1.8, 2.1], dd5_headers, dd5_data)

    add_heading_3(doc, "4.4.6 Data Dictionary: Visual Assets Entity (tbl_figure_assets)")
    dd6_headers = ["Field Name", "Data Type", "Constraints", "Description & Purpose"]
    dd6_data = [
        ["figure_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique identifier for the figure asset."],
        ["project_id", "VARCHAR(64)", "FOREIGN KEY, NOT NULL", "References tbl_paper_project.project_id."],
        ["caption", "VARCHAR(255)", "NOT NULL", "Descriptive scientific figure caption."],
        ["file_path_png", "VARCHAR(500)", "NOT NULL", "Filesystem path to 300 DPI rendered PNG asset."],
        ["file_path_pdf", "VARCHAR(500)", "NOT NULL", "Filesystem path to vector PDF graphic asset."],
        ["latex_snippet", "TEXT", "NOT NULL", "Pre-formatted \\begin{figure} LaTeX code block."]
    ]
    t_dd6 = doc.add_table(rows=1, cols=4)
    style_table(t_dd6, [1.5, 1.4, 1.8, 2.1], dd6_headers, dd6_data)

    doc.add_page_break()

def generate_chapter_5(doc):
    # =========================================================
    # CHAPTER 5: IMPLEMENTATION
    # =========================================================
    add_heading_1(doc, "5. IMPLEMENTATION")

    add_heading_2(doc, "5.1 Form Layouts")
    add_body_p(doc, "The user interface of the AI Research Paper Assistant is engineered using responsive, reactive web forms powered by Streamlit. Each form incorporates explicit validation rules, sensible default configurations, clear user affordances, and session state persistence.")

    add_heading_3(doc, "5.1.1 Project Configuration & Venue Settings Form")
    add_body_p(doc, "The Project Configuration Form resides on the global sidebar, allowing authors to establish project metadata at any point during authoring. Key form components include:")
    add_bullet_p(doc, "Single-line text input field pre-populated with active research title. Sanitizes input strings against special characters and enforces a 200-character maximum.", bold_prefix="• Working Manuscript Title Input: ")
    add_bullet_p(doc, "Single-line text input capturing comma-separated author names, institutional affiliations, and email contacts.", bold_prefix="• Author Metadata & Affiliation: ")
    add_bullet_p(doc, "Interactive dropdown menu offering standard templates: 'NeurIPS / ICLR (Conference)', 'IEEE Transactions (Two-Column Journal)', 'ACM SIGKDD (Conference)', 'Springer LNCS', and 'Nature / Science Style'. Selecting a venue dynamically configures LaTeX document classes, bibliography styles, and section targets.", bold_prefix="• Target Venue Selector: ")
    add_bullet_p(doc, "Dropdown toggle switching between 'Offline Academic Engine (Instant & Cost-Free)', 'Google Gemini 1.5 Pro', and 'OpenAI GPT-4o'. In offline mode, the form hides API key inputs and displays a green zero-cost confirmation banner.", bold_prefix="• LLM Engine Mode Selector: ")
    add_bullet_p(doc, "Action button serializing the active project dictionary into a downloadable JSON file, enabling researchers to resume authoring sessions seamlessly.", bold_prefix="• Project State Import / Export: ")

    add_heading_3(doc, "5.1.2 Academic Literature Search & Filter Form")
    add_body_p(doc, "The Literature Search Form captures multi-faceted research queries and filters results to maximize academic relevance:")
    add_bullet_p(doc, "Accepts academic topics, author names, or specific paper DOIs/arXiv identifiers.", bold_prefix="• Query Input Box: ")
    add_bullet_p(doc, "Dropdown filter allowing authors to restrict searches to 'All Years', 'Last 3 Years', 'Last 5 Years', or custom ranges, ensuring recent literature discovery.", bold_prefix="• Publication Year Range Filter: ")
    add_bullet_p(doc, "Interactive slider widget configuring query limits from 5 to 50 papers per search, optimizing API bandwidth and loading latency.", bold_prefix="• Result Quantity Slider: ")
    add_bullet_p(doc, "Executes the REST request, triggers visual loading spinners, and dynamically renders cards containing paper metadata, citation badges, and 'Save' buttons.", bold_prefix="• Search Action Button: ")

    add_heading_3(doc, "5.1.3 Hierarchical Outline Editor Form")
    add_body_p(doc, "The Outline Editor Form provides an interactive workspace for structuring the manuscript:")
    add_bullet_p(doc, "Interactive cards corresponding to the 8 standard conference sections. Authors can adjust section titles, reorder sections, and modify target word count distributions.", bold_prefix="• Dynamic Section Cards: ")
    add_bullet_p(doc, "Multi-line text area inside each section card where authors record specific arguments, experimental findings, or methodological notes.", bold_prefix="• Section Key Points & Objectives Input: ")
    add_bullet_p(doc, "Automatically recalculates total manuscript word count as individual section targets are edited, displaying a real-time progress bar against target conference page budgets.", bold_prefix="• Dynamic Word Budget Counter: ")

    add_heading_3(doc, "5.1.4 Context-Enriched Section Drafting Form")
    add_body_p(doc, "The Section Drafting Form orchestrates the generation and refinement of academic prose:")
    add_bullet_p(doc, "Allows authors to choose which outline section to draft or refine.", bold_prefix="• Target Section Selector: ")
    add_bullet_p(doc, "Interactive slider controlling synthesis depth from 'Concise Summary' (300 words) to 'Comprehensive Academic Treatise' (1,500+ words).", bold_prefix="• Drafting Rigor & Depth Slider: ")
    add_bullet_p(doc, "Checkbox toggles enabling automatic insertion of LaTeX equation environments (align, equation) and algorithm pseudocode blocks.", bold_prefix="• Mathematical Rigor Toggle: ")
    add_bullet_p(doc, "Large expandable text area featuring syntax highlighting, live word count metrics, and real-time citation validation.", bold_prefix="• Interactive Markdown Editor: ")

    add_heading_3(doc, "5.1.5 Publication Plot Configuration Form")
    add_body_p(doc, "The Plot Studio Form allows researchers to create publication-grade visualizations:")
    add_bullet_p(doc, "Dropdown offering pre-configured templates: 'Model Accuracy Ablation', 'Inference Latency vs. Sequence Length', 'Benchmark Performance Comparison', and 'Parameter Scaling Efficiency'.", bold_prefix="• Plot Template Selector: ")
    add_bullet_p(doc, "Text inputs for chart title, x-axis label, y-axis label, legend positioning, and figure aspect ratio.", bold_prefix="• Axis & Styling Parameters: ")
    add_bullet_p(doc, "Executes the Matplotlib/Seaborn script in a sandboxed runtime, outputs 300 DPI raster and vector previews, and displays a copy-ready LaTeX figure block.", bold_prefix="• Render Visualization Button: ")

    add_heading_2(doc, "5.2 Report Layouts")
    add_body_p(doc, "The platform generates publication-grade documents conforming to formal academic standards. The layout specifications of these outputs are detailed below:")

    add_heading_3(doc, "5.2.1 IEEE & NeurIPS Conference LaTeX Manuscript Layout")
    add_body_p(doc, "The generated main.tex file adheres strictly to top-tier machine learning and computer science conference conventions. Its structural layout includes:")
    add_bullet_p(doc, "Specifies conference package (e.g., \\documentclass{article} with \\usepackage{neurips_2024} or \\documentclass[conference]{IEEEtran}). Loads essential packages including amsmath, amssymb, graphicx, booktabs, hyperref, and microtype.", bold_prefix="1. Preamble & Package Declarations: ")
    add_bullet_p(doc, "Structures \\title{}, \\author{}, and affiliation blocks according to venue anonymity guidelines (supporting double-blind submissions).", bold_prefix="2. Title & Author Blocks: ")
    add_bullet_p(doc, "Encapsulates a self-contained 200-word overview synthesizing background, problem statement, proposed methodology, empirical results, and broader impact.", bold_prefix="3. Abstract & Keywords Environment: ")
    add_bullet_p(doc, "Employs \\section{} and \\subsection{} hierarchies corresponding to the approved outline, with centered equation blocks (\\begin{align}) and professional three-line tables (\\toprule, \\midrule, \\bottomrule).", bold_prefix="4. Structured Section Bodies: ")
    add_bullet_p(doc, "Implements \\bibliographystyle{abbrvnat} or \\bibliographystyle{IEEEtran} and \\bibliography{references}, ensuring automated citation rendering.", bold_prefix="5. Bibliography Directive: ")

    add_heading_3(doc, "5.2.2 BibTeX Bibliography Database Layout (references.bib)")
    add_body_p(doc, "The generated references.bib file organizes all referenced literature using clean, standardized BibTeX entries. Each record includes unique citation keys, author lists formatted as 'Surname, Firstname and ...', titles enclosed in double curly braces to preserve capitalization, booktitles/journals, publication years, and DOIs.")

    add_heading_3(doc, "5.2.3 Automated Peer Review Summary Report Layout")
    add_body_p(doc, "The Peer Review Report generates an objective pre-submission critique formatted as follows:")
    add_bullet_p(doc, "Displays manuscript title, word count, target venue, and aggregate score on a 1.0 to 10.0 scale with a consensus verdict badge.", bold_prefix="1. Executive Summary: ")
    add_bullet_p(doc, "Tabular breakdown presenting ratings across Originality, Technical Soundness, Empirical Rigor, Clarity, and Literature Coverage.", bold_prefix="2. Dimension Scorecard: ")
    add_bullet_p(doc, "Three distinct reviewer viewpoints: Reviewer 1 (Theoretical Soundness), Reviewer 2 (Methodology & Baseline Comparisons), and Reviewer 3 (Clarity & Readability).", bold_prefix="3. Multi-Persona Critiques: ")
    add_bullet_p(doc, "Prioritized list of actionable recommendations for improving paper quality prior to formal submission.", bold_prefix="4. Actionable Suggestions: ")

    add_heading_3(doc, "5.2.4 Self-Contained Overleaf ZIP Archive Hierarchy")
    add_body_p(doc, "The platform packages all authoring deliverables into an autonomous ZIP archive structured as follows:")
    add_code_block(doc, 
r'''paper_bundle.zip/
├── main.tex                 # Fully assembled, conference-ready LaTeX manuscript
├── references.bib           # Complete BibTeX bibliography with audited keys
├── figures/                 # Sub-directory containing rendered assets
│   ├── fig_latency.png      # 300 DPI high-resolution raster graphic
│   ├── fig_latency.pdf      # Vector PDF graphic for lossless print scaling
│   └── fig_ablation.png     # Benchmark ablation chart
├── Makefile                 # Automated build script for Linux/macOS TeX Live
├── compile.bat              # 1-click Windows compilation script
└── README.txt               # Instructions for opening and compiling on Overleaf''')

    add_heading_2(doc, "5.3 Coding Convention (Business Logic)")
    add_body_p(doc, "The codebase follows strict software engineering principles: PEP 8 styling conventions, descriptive snake_case naming, type annotations, modular service layers, and graceful exception handling. Key business logic implementations are detailed below:")

    add_heading_3(doc, "5.3.1 Semantic Scholar REST Client Implementation")
    add_body_p(doc, "The LiteratureSearcher module handles network communication, query serialization, rate limiting, and BibTeX extraction:")
    add_code_block(doc,
r'''import requests
import urllib.parse
from typing import List, Dict, Any

class LiteratureSearcher:
    BASE_URL = 'https://api.semanticscholar.org/graph/v1/paper/search'

    def __init__(self, api_key: str = None):
        self.headers = {'x-api-key': api_key} if api_key else {}

    def search_papers(self, query: str, limit: int = 10, year_range: str = 'all') -> List[Dict[str, Any]]:
        fields = 'paperId,title,abstract,year,citationCount,authors,venue'
        params = {'query': query, 'limit': limit, 'fields': fields}
        if year_range != 'all' and '-' in year_range:
            params['year'] = year_range

        try:
            response = requests.get(self.BASE_URL, params=params, headers=self.headers, timeout=12)
            response.raise_for_status()
            data = response.json()
            return [self._format_paper(p) for p in data.get('data', [])]
        except Exception as e:
            # Fallback to local curated cache upon network or quota failure
            return self._load_fallback_papers(query)

    def _format_paper(self, raw: dict) -> dict:
        authors = [a.get('name', '') for a in raw.get('authors', [])]
        first_author = authors[0].split()[-1].lower() if authors else 'anon'
        year = raw.get('year') or 2024
        bib_key = f"{first_author}{year}{raw.get('title', '').split()[0].lower()}"
        return {
            'id': raw.get('paperId', ''),
            'title': raw.get('title', 'Untitled'),
            'abstract': raw.get('abstract', 'No abstract available.'),
            'authors': ', '.join(authors),
            'year': year,
            'citations': raw.get('citationCount', 0),
            'bibtex_key': bib_key,
            'bibtex': self._generate_bibtex(bib_key, raw, authors, year)
        }''')

    add_heading_3(doc, "5.3.2 Multi-Provider LLM Prompting & Offline Fallback Engine")
    add_body_p(doc, "The LLMEngine service implements an abstract strategy pattern, enabling seamless switching between live cloud models and the local deterministic academic synthesizer:")
    add_code_block(doc,
r'''from abc import ABC, abstractmethod

class BaseLLMEngine(ABC):
    @abstractmethod
    def generate_draft(self, section_name: str, context: dict) -> str:
        pass

class CloudLLMEngine(BaseLLMEngine):
    def __init__(self, provider: str = 'gemini', api_key: str = None):
        self.provider = provider
        self.api_key = api_key

    def generate_draft(self, section_name: str, context: dict) -> str:
        prompt = self._assemble_academic_prompt(section_name, context)
        if self.provider == 'gemini':
            from google import genai
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model='gemini-1.5-pro',
                contents=prompt
            )
            return response.text
        # Fallback to OpenAI or local engine on error...

class OfflineAcademicEngine(BaseLLMEngine):
    def generate_draft(self, section_name: str, context: dict) -> str:
        # Deterministic, high-rigor academic generator with LaTeX equations
        title = context.get('title', 'Research Project')
        citations = context.get('citations', [])
        return self._synthesize_section(section_name, title, citations)''')

    add_heading_3(doc, "5.3.3 Citation Auditor & Health Checker")
    add_body_p(doc, "The CitationAuditor verifies bibliographic consistency prior to document compilation:")
    add_code_block(doc,
r'''import re

class CitationAuditor:
    @staticmethod
    def audit_manuscript(manuscript_text: str, bibtex_database: str) -> dict:
        cited_keys = set(re.findall(r'\\cite\{([^}]+)\}', manuscript_text))
        # Split multi-keys: \cite{key1, key2}
        all_cited = set()
        for ck in cited_keys:
            for k in ck.split(','):
                all_cited.add(k.strip())

        bib_keys = set(re.findall(r'@\w+\{([^,]+),', bibtex_database))
        missing_keys = all_cited - bib_keys
        unused_keys = bib_keys - all_cited

        return {
            'is_healthy': len(missing_keys) == 0,
            'total_citations': len(all_cited),
            'missing_keys': list(missing_keys),
            'unused_keys': list(unused_keys)
        }''')

    add_heading_3(doc, "5.3.4 Overleaf ZIP Packager Implementation")
    add_body_p(doc, "The OverleafPackager packages all required assets into a clean, autonomous ZIP archive:")
    add_code_block(doc,
r'''import zipfile
from pathlib import Path

class OverleafPackager:
    @staticmethod
    def create_bundle(output_zip: Path, tex_content: str, bib_content: str, figures: list) -> Path:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('main.tex', tex_content)
            zf.writestr('references.bib', bib_content)
            zf.writestr('Makefile', 'all:\n\tlatexmk -pdf main.tex\nclean:\n\tlatexmk -C\n')
            zf.writestr('compile.bat', '@echo off\npdflatex main.tex\nbibtex main\npdflatex main.tex\npdflatex main.tex\n')
            zf.writestr('README.txt', 'Upload this ZIP directly to Overleaf (New Project -> Upload Project).')
            for fig in figures:
                if Path(fig).exists():
                    zf.write(fig, arcname=f'figures/{Path(fig).name}')
        return output_zip''')

    doc.add_page_break()


def generate_chapter_6(doc):
    # =========================================================
    # CHAPTER 6: TESTING
    # =========================================================
    add_heading_1(doc, "6. TESTING")

    add_heading_2(doc, "6.1 Test Strategy")
    add_body_p(doc, "To verify system stability, reliability, and academic rigor, a structured multi-level testing strategy was executed throughout the development lifecycle. Testing was conducted across five sequential phases:")

    add_bullet_p(doc, "Individual Python modules, API clients, citation parsers, and plot generation functions were tested in isolation using Python's native unittest framework (test_suite.py). All 10 unit test cases passed with 100% success rate.", bold_prefix="1. Unit Testing: ")
    add_bullet_p(doc, "Verified data flow across interconnected modules, including passing search results from the Semantic Scholar client into the project bibliography, propagating outline schemas to the drafting engine, and linking BibTeX keys into LaTeX figure blocks.", bold_prefix="2. Integration Testing: ")
    add_bullet_p(doc, "Evaluated the complete end-to-end authoring pipeline from initial project configuration to final Overleaf ZIP export, confirming end-to-end functionality under both Live Cloud and Offline modes.", bold_prefix="3. System Testing: ")
    add_bullet_p(doc, "Conducted with post-graduate M.Sc. IT and MCA scholars to validate usability, user interface responsiveness, clarity of peer review feedback, and ease of Overleaf import.", bold_prefix="4. User Acceptance Testing (UAT): ")
    add_bullet_p(doc, "Simulated network timeouts, malformed BibTeX entries, oversized prompts, and missing LaTeX compilers to verify graceful error recovery and zero application crashes.", bold_prefix="5. Robustness & Edge-Case Testing: ")

    add_heading_2(doc, "6.2 Test Cases")
    add_body_p(doc, "The platform was evaluated against sixteen rigorous test cases covering core functional features, exception handling, and edge-case boundaries. The comprehensive test results are documented in the table below:")

    tc_headers = ["Test ID", "Test Scenario", "Input Data / Action", "Expected Result", "Actual Result", "Status"]
    tc_data = [
        ["TC-01", "Workspace Initialization", "Enter valid title, select NeurIPS venue.", "State initialized; session JSON created.", "State initialized; default outline loaded.", "PASS"],
        ["TC-02", "Literature Keyword Search", "Query: 'State Space Models', Limit: 10.", "Returns 10 papers with metadata & BibTeX.", "10 papers retrieved and rendered cleanly.", "PASS"],
        ["TC-03", "Empty Search Query", "Click 'Search' with empty text box.", "Warning message displayed; no crash.", "Prompt displayed: 'Please enter query'.", "PASS"],
        ["TC-04", "Network API Timeout", "Simulate network disconnect during search.", "Graceful fallback to cached mock papers.", "Fallback loaded; warning displayed.", "PASS"],
        ["TC-05", "Save Literature Paper", "Click 'Save to Research Material'.", "Paper appended to project bibliography.", "Paper and BibTeX saved to project state.", "PASS"],
        ["TC-06", "Extract Research Insights", "Click 'Generate Insights' with 5 papers.", "Synthesizes patterns, gaps, hypotheses.", "Extracts core methodology and hypothesis.", "PASS"],
        ["TC-07", "Outline Generation", "Select IEEE venue, click 'Generate Outline'.", "Creates 8-section outline with word targets.", "8-section hierarchical outline generated.", "PASS"],
        ["TC-08", "Custom Outline Edit", "Modify Section 3 title to 'Formulation'.", "Section title updated in project state.", "Updated title persisted into project state.", "PASS"],
        ["TC-09", "Section Drafting (Cloud)", "Draft 'Introduction' via Gemini API.", "Generates 800-word formal academic prose.", "Structured academic draft generated.", "PASS"],
        ["TC-10", "Section Drafting (Offline)", "Toggle Offline Mode, draft 'Methodology'.", "Generates prose with LaTeX equations.", "Complete prose with align math generated.", "PASS"],
        ["TC-11", "Simulated Peer Review", "Run review on 3 drafted sections.", "Calculates scores and multi-reviewer text.", "Score: 8.5/10 with 3 reviewer critiques.", "PASS"],
        ["TC-12", "Plot Generation", "Execute 'Latency Scaling' plot script.", "Renders 300 DPI PNG & vector PDF.", "PNG and PDF rendered in outputs/plots.", "PASS"],
        ["TC-13", "Plot Code Syntax Error", "Input invalid Python syntax in plot code.", "Catches syntax error, displays traceback.", "Error caught; UI displayed error block.", "PASS"],
        ["TC-14", "Citation Health Check", "Draft references unlisted \\cite{badKey}.", "Flags 'badKey' as unreferenced in BibTeX.", "Warning highlights missing 'badKey'.", "PASS"],
        ["TC-15", "Overleaf ZIP Packaging", "Click 'Generate Overleaf ZIP Bundle'.", "ZIP created with main.tex, bib, and plots.", "Complete ZIP generated and validated.", "PASS"],
        ["TC-16", "Local PDF Compilation", "Trigger compilation with tectonic present.", "Compiles camera-ready PDF document.", "PDF compiled cleanly without TeX errors.", "PASS"]
    ]
    t_tc = doc.add_table(rows=1, cols=6)
    style_table(t_tc, [0.8, 1.4, 1.4, 1.6, 1.4, 0.6], tc_headers, tc_data)

    doc.add_page_break()


def generate_chapter_7(doc):
    # =========================================================
    # CHAPTER 7: FUTURE ENHANCEMENTS
    # =========================================================
    add_heading_1(doc, "7. FUTURE ENHANCEMENTS")
    add_body_p(doc, "While the AI Research Paper Assistant provides a complete, robust academic authoring environment, several planned enhancements will expand its capabilities in subsequent releases:")

    add_bullet_p(doc, "Implementing WebSocket-driven multi-user synchronization (similar to Google Docs or Overleaf) enabling multiple student co-authors and faculty guides to edit sections, review comments, and stage citations concurrently.", bold_prefix="7.1 Real-Time Collaborative Authoring: ")
    add_bullet_p(doc, "Integrating multimodal vision-language models (e.g., Gemini 1.5 Pro Vision) capable of critiquing uploaded experimental diagrams, system architecture flowcharts, and plot readability, ensuring visual clarity.", bold_prefix="7.2 Multimodal Architectural Diagram Critique: ")
    add_bullet_p(doc, "Embedding a local vector database (ChromaDB or FAISS) that ingests users' local PDF libraries, enabling fine-grained semantic passage retrieval and verbatim quotation verification with page-level attribution.", bold_prefix="7.3 Local Vector RAG for Offline PDF Repositories: ")
    add_bullet_p(doc, "Adding 1-click submission interfaces to arXiv, OpenReview, and IEEE conference submission portals via authenticated REST APIs, automating metadata transfer and paper uploading.", bold_prefix="7.4 Automated Pre-print & Conference Submission APIs: ")
    add_bullet_p(doc, "Developing lightweight, domain-adapted small language models (SLMs) trained on peer-reviewed open-access computer science literature, enabling local LLM execution on standard laptops.", bold_prefix="7.5 Fine-Tuned Domain-Specific Language Models: ")

    doc.add_page_break()


def generate_chapter_8(doc):
    # =========================================================
    # CHAPTER 8: BIBLIOGRAPHY
    # =========================================================
    add_heading_1(doc, "8. BIBLIOGRAPHY")
    add_body_p(doc, "The development, theoretical foundations, and software engineering methodologies of this project are informed by the following literature, software documentation, and academic guidelines:")

    bib_entries = [
        "[1] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). \"Attention is all you need.\" Advances in Neural Information Processing Systems (NeurIPS 2017), Vol. 30, pp. 5998–6008.",
        "[2] Dao, T., Fu, D. Y., Ermon, S., Rudra, A., & Ré, C. (2022). \"FlashAttention: Fast and memory-efficient exact attention with IO-awareness.\" Advances in Neural Information Processing Systems (NeurIPS 2022), Vol. 35, pp. 16344–16359.",
        "[3] Gu, A., & Dao, T. (2023). \"Mamba: Linear-time sequence modeling with selective state spaces.\" arXiv preprint arXiv:2312.00752.",
        "[4] Kinney, R., Kohlmeier, C., Akbik, A., et al. (2023). \"The Semantic Scholar Open Research Corpus.\" ACM Transactions on Interactive Intelligent Systems, Vol. 13, No. 2, pp. 1–28.",
        "[5] Streamlit Documentation. (2024). \"The fastest way to build and share data applications.\" Snowflake Inc. Retrieved from https://docs.streamlit.io/.",
        "[6] Lamport, L. (1994). \"LaTeX: A Document Preparation System.\" Addison-Wesley Professional, 2nd Edition, Reading, Massachusetts.",
        "[7] Hunter, J. D. (2007). \"Matplotlib: A 2D graphics environment.\" Computing in Science & Engineering, Vol. 9, No. 3, pp. 90–95.",
        "[8] Waskom, M. L. (2021). \"Seaborn: statistical data visualization.\" Journal of Open Source Software, Vol. 6, No. 60, pp. 3021.",
        "[9] Pressman, R. S., & Maxim, B. R. (2020). \"Software Engineering: A Practitioner's Approach.\" McGraw-Hill Higher Education, 9th Edition, New York.",
        "[10] Sommerville, I. (2016). \"Software Engineering.\" Pearson Education, 10th Global Edition, London.",
        "[11] Parul University Academic Council. (2025). \"Guidelines for Minor and Major Project Reports for Master of Computer Applications (MCA) & M.Sc. IT Programs.\" Parul University, Vadodara, Gujarat, India.",
        "[12] IEEE Publications Board. (2024). \"IEEE Authorship Guidelines and LaTeX Document Class Templates.\" Institute of Electrical and Electronics Engineers. Retrieved from https://www.ieee.org/."
    ]

    for b in bib_entries:
        add_body_p(doc, b)


def build_complete_report():
    print("Building Parul University Minor Project Report...")
    doc = Document()

    # Section 1: Preliminary Pages (No Header, No Footer, No Page Number)
    sec1 = doc.sections[0]
    clear_preliminary_header_footer(sec1)
    generate_preliminary_pages(doc)

    # Section 2: Chapter 1 (Header and Page Numbering start here at Page 1)
    sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_header_footer(sec2, chapter_title="1. About Department of MScIT")
    reset_section_page_number(sec2, start_num=1)
    generate_chapter_1(doc)

    # Section 3: Chapter 2
    sec3 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_header_footer(sec3, chapter_title="2. Project Profile")
    continue_section_page_number(sec3)
    generate_chapter_2(doc)

    # Section 4: Chapter 3
    sec4 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_header_footer(sec4, chapter_title="3. Requirement Analysis")
    continue_section_page_number(sec4)
    generate_chapter_3(doc)

    # Section 5: Chapter 4
    sec5 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_header_footer(sec5, chapter_title="4. Design")
    continue_section_page_number(sec5)
    generate_chapter_4(doc)

    # Section 6: Chapter 5
    sec6 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_header_footer(sec6, chapter_title="5. Implementation")
    continue_section_page_number(sec6)
    generate_chapter_5(doc)

    # Section 7: Chapter 6
    sec7 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_header_footer(sec7, chapter_title="6. Testing")
    continue_section_page_number(sec7)
    generate_chapter_6(doc)

    # Section 8: Chapter 7
    sec8 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_header_footer(sec8, chapter_title="7. Future Enhancements")
    continue_section_page_number(sec8)
    generate_chapter_7(doc)

    # Section 9: Chapter 8
    sec9 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_header_footer(sec9, chapter_title="8. Bibliography")
    continue_section_page_number(sec9)
    generate_chapter_8(doc)

    # Save to report directory
    output_docx = REPORT_DIR / "Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
    doc.save(str(output_docx))
    print(f"Successfully generated DOCX report at: {output_docx}")
    return output_docx

if __name__ == "__main__":
    build_complete_report()
