"""
Complete End-to-End Pipeline:
1. Generate initial document
2. Scan exact page numbers with Word COM
3. Regenerate document with synchronized Index
4. Export camera-ready PDF with Word COM
5. Verify PDF integrity with pypdf
6. Distribute to Desktop and Downloads
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import pypdf

from generate_perfect_report import build_report_doc, REPORT_DIR, DESKTOP_DIR, DOWNLOADS_DIR, BASE_DIR

FINAL_DOCX_NAME = "Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
FINAL_PDF_NAME = "Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.pdf"

def step_1_generate_draft():
    print("[1/5] Generating initial draft document...")
    doc = build_report_doc(page_map=None)
    draft_path = REPORT_DIR / "draft_report.docx"
    doc.save(str(draft_path))
    print(f"Draft saved to {draft_path}")
    return draft_path

def step_2_scan_pages(docx_path):
    print("[2/5] Scanning exact adjusted page numbers via Word COM...")
    ps_script = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open('{docx_path}')
$doc.Fields.Update()

$targets = @(
    @{{ key = "ch1"; prefix = "1. ABOUT DEPARTMENT OF MScIT" }},
    @{{ key = "s1_1"; prefix = "1.1 Overview of Department" }},
    @{{ key = "s1_2"; prefix = "1.2 Department Vision" }},
    @{{ key = "s1_3"; prefix = "1.3 State-of-the-Art" }},
    @{{ key = "s1_4"; prefix = "1.4 Academic Relevance" }},
    @{{ key = "ch2"; prefix = "2. PROJECT PROFILE" }},
    @{{ key = "s2_1"; prefix = "2.1 Project Definition" }},
    @{{ key = "s2_2"; prefix = "2.2 Project Description" }},
    @{{ key = "s2_3"; prefix = "2.3 Existing System" }},
    @{{ key = "s2_4"; prefix = "2.4 Problem Statements" }},
    @{{ key = "s2_5"; prefix = "2.5 Need for New System" }},
    @{{ key = "s2_6"; prefix = "2.6 Proposed System" }},
    @{{ key = "s2_7"; prefix = "2.7 Scope" }},
    @{{ key = "s2_8"; prefix = "2.8 Outcomes" }},
    @{{ key = "s2_9"; prefix = "2.9 Tools & Technology" }},
    @{{ key = "s2_10"; prefix = "2.10 Project Plan" }},
    @{{ key = "ch3"; prefix = "3. REQUIREMENT ANALYSIS" }},
    @{{ key = "s3_1"; prefix = "3.1 Feasibility Study" }},
    @{{ key = "s3_2"; prefix = "3.2 Users of the System" }},
    @{{ key = "s3_3"; prefix = "3.3 Modules" }},
    @{{ key = "s3_4"; prefix = "3.4 Process Model" }},
    @{{ key = "s3_5"; prefix = "3.5 Hardware & Software" }},
    @{{ key = "s3_6"; prefix = "3.6 Use Cases" }},
    @{{ key = "s3_7"; prefix = "3.7 Use Case Diagram" }},
    @{{ key = "ch4"; prefix = "4. DESIGN" }},
    @{{ key = "s4_1"; prefix = "4.1 Use Case Scenarios" }},
    @{{ key = "s4_2"; prefix = "4.2 Diagrams" }},
    @{{ key = "s4_2_1"; prefix = "4.2.1 UML and Data Flow Diagrams" }},
    @{{ key = "s4_2_2"; prefix = "4.2.2 Entity Relationship Diagram" }},
    @{{ key = "s4_3"; prefix = "4.3 Screenshots of Website" }},
    @{{ key = "s4_4"; prefix = "4.4 Data Dictionary" }},
    @{{ key = "ch5"; prefix = "5. IMPLEMENTATION" }},
    @{{ key = "s5_1"; prefix = "5.1 Form Layouts" }},
    @{{ key = "s5_2"; prefix = "5.2 Report Layouts" }},
    @{{ key = "s5_3"; prefix = "5.3 Coding Convention" }},
    @{{ key = "ch6"; prefix = "6. TESTING" }},
    @{{ key = "s6_1"; prefix = "6.1 Test Strategy" }},
    @{{ key = "s6_2"; prefix = "6.2 Test Cases" }},
    @{{ key = "ch7"; prefix = "7. FUTURE ENHANCEMENTS" }},
    @{{ key = "ch8"; prefix = "8. BIBLIOGRAPHY" }},
    @{{ key = "ch9"; prefix = "9. APPENDICES" }},
    @{{ key = "app_a"; prefix = "Appendix A: System Architecture" }},
    @{{ key = "app_b"; prefix = "Appendix B: Standalone Database" }}
)

$pageMap = @{{}}
foreach ($para in $doc.Paragraphs) {{
    $phys = $para.Range.Information(3)
    if ($phys -ge 7) {{
        $txt = $para.Range.Text.Trim()
        if ($txt.Length -gt 0) {{
            foreach ($item in $targets) {{
                if (-not $pageMap.ContainsKey($item.key)) {{
                    if ($txt.StartsWith($item.prefix)) {{
                        $adj = $para.Range.Information(1)
                        $pageMap[$item.key] = $adj
                        Write-Output "$($item.key) -> Page $adj (Phys $phys)"
                        break
                    }}
                }}
            }}
        }}
    }}
}}

$jsonPath = "C:\\Users\\anand\\.gemini\\antigravity\\scratch\\ai_research_paper_assistant\\scanned_pages.json"
$pageMap | ConvertTo-Json | Set-Content -Path $jsonPath -Encoding utf8

$doc.Close(0)
$word.Quit()
"""
    ps_file = BASE_DIR / "run_scan.ps1"
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)

    res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_file)], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("STDERR:", res.stderr)

    json_path = BASE_DIR / "scanned_pages.json"
    with open(json_path, "r", encoding="utf-8-sig") as f:
        page_map = json.load(f)
    print(f"Scanned {len(page_map)} heading pages successfully.")
    return page_map

def step_3_generate_final_docx(page_map):
    print("[3/5] Generating finalized Word document with exact Index numbers...")
    doc = build_report_doc(page_map=page_map)
    final_docx = REPORT_DIR / FINAL_DOCX_NAME
    doc.save(str(final_docx))
    print(f"Final Word Document saved to {final_docx}")
    return final_docx

def step_4_export_pdf(docx_path):
    print("[4/5] Updating Word fields and exporting camera-ready PDF...")
    final_pdf = REPORT_DIR / FINAL_PDF_NAME
    ps_export = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open('{docx_path}')
$doc.Fields.Update()
$pdfPath = '{final_pdf}'
$doc.ExportAsFixedFormat($pdfPath, 17)
$pages = $doc.ComputeStatistics(2)
Write-Output "Word reports total physical pages: $pages"
$doc.Close(0)
$word.Quit()
Write-Output "PDF Export completed successfully."
"""
    ps_file = BASE_DIR / "run_export.ps1"
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_export)

    res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_file)], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("STDERR:", res.stderr)

    return final_pdf

def step_5_verify_and_distribute(docx_path, pdf_path, page_map):
    print("[5/5] Verifying PDF structure and distributing deliverables...")
    reader = pypdf.PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    print(f"PDF verified: {total_pages} total physical pages.")

    # Distribute to Desktop, Downloads, and scratch root
    targets = [
        DESKTOP_DIR / FINAL_DOCX_NAME,
        DESKTOP_DIR / FINAL_PDF_NAME,
        DOWNLOADS_DIR / FINAL_DOCX_NAME,
        DOWNLOADS_DIR / FINAL_PDF_NAME,
        BASE_DIR / FINAL_DOCX_NAME,
        BASE_DIR / FINAL_PDF_NAME,
    ]

    for t in targets:
        src = docx_path if t.suffix == ".docx" else pdf_path
        shutil.copy2(src, t)
        print(f"Delivered -> {t} ({t.stat().st_size} bytes)")

    print("\nALL TASKS COMPLETED SUCCESSFULLY!")

def main():
    draft = step_1_generate_draft()
    page_map = step_2_scan_pages(draft)
    final_docx = step_3_generate_final_docx(page_map)
    final_pdf = step_4_export_pdf(final_docx)
    step_5_verify_and_distribute(final_docx, final_pdf, page_map)

if __name__ == "__main__":
    main()
