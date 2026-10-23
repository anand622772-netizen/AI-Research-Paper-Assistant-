$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\parul_university_report\test_report.docx"
$doc = $word.Documents.Open($docPath)
$doc.Fields.Update()

Write-Output "Scanning headings in Word..."

$targets = @(
    @{ key = "ch1"; prefix = "1. ABOUT DEPARTMENT OF MScIT" },
    @{ key = "s1_1"; prefix = "1.1 Overview of Department" },
    @{ key = "s1_2"; prefix = "1.2 Department Vision" },
    @{ key = "s1_3"; prefix = "1.3 State-of-the-Art" },
    @{ key = "s1_4"; prefix = "1.4 Academic Relevance" },
    @{ key = "ch2"; prefix = "2. PROJECT PROFILE" },
    @{ key = "s2_1"; prefix = "2.1 Project Definition" },
    @{ key = "s2_2"; prefix = "2.2 Project Description" },
    @{ key = "s2_3"; prefix = "2.3 Existing System" },
    @{ key = "s2_4"; prefix = "2.4 Problem Statements" },
    @{ key = "s2_5"; prefix = "2.5 Need for New System" },
    @{ key = "s2_6"; prefix = "2.6 Proposed System" },
    @{ key = "s2_7"; prefix = "2.7 Scope" },
    @{ key = "s2_8"; prefix = "2.8 Outcomes" },
    @{ key = "s2_9"; prefix = "2.9 Tools & Technology" },
    @{ key = "s2_10"; prefix = "2.10 Project Plan" },
    @{ key = "ch3"; prefix = "3. REQUIREMENT ANALYSIS" },
    @{ key = "s3_1"; prefix = "3.1 Feasibility Study" },
    @{ key = "s3_2"; prefix = "3.2 Users of the System" },
    @{ key = "s3_3"; prefix = "3.3 Modules" },
    @{ key = "s3_4"; prefix = "3.4 Process Model" },
    @{ key = "s3_5"; prefix = "3.5 Hardware & Software" },
    @{ key = "s3_6"; prefix = "3.6 Use Cases" },
    @{ key = "s3_7"; prefix = "3.7 Use Case Diagram" },
    @{ key = "ch4"; prefix = "4. DESIGN" },
    @{ key = "s4_1"; prefix = "4.1 Use Case Scenarios" },
    @{ key = "s4_2"; prefix = "4.2 Diagrams" },
    @{ key = "s4_2_1"; prefix = "4.2.1 UML and Data Flow Diagrams" },
    @{ key = "s4_2_2"; prefix = "4.2.2 Entity Relationship Diagram" },
    @{ key = "s4_3"; prefix = "4.3 Screenshots of Website" },
    @{ key = "s4_4"; prefix = "4.4 Data Dictionary" },
    @{ key = "ch5"; prefix = "5. IMPLEMENTATION" },
    @{ key = "s5_1"; prefix = "5.1 Form Layouts" },
    @{ key = "s5_2"; prefix = "5.2 Report Layouts" },
    @{ key = "s5_3"; prefix = "5.3 Coding Convention" },
    @{ key = "ch6"; prefix = "6. TESTING" },
    @{ key = "s6_1"; prefix = "6.1 Test Strategy" },
    @{ key = "s6_2"; prefix = "6.2 Test Cases" },
    @{ key = "ch7"; prefix = "7. FUTURE ENHANCEMENTS" },
    @{ key = "ch8"; prefix = "8. BIBLIOGRAPHY" },
    @{ key = "ch9"; prefix = "9. APPENDICES" },
    @{ key = "app_a"; prefix = "Appendix A: System Architecture" },
    @{ key = "app_b"; prefix = "Appendix B: Standalone Database" }
)

$pageMap = @{}

foreach ($para in $doc.Paragraphs) {
    # Check physical page first; only consider body paragraphs (physical page >= 7)
    $phys = $para.Range.Information(3)
    if ($phys -ge 7) {
        $txt = $para.Range.Text.Trim()
        if ($txt.Length -gt 0) {
            foreach ($item in $targets) {
                if (-not $pageMap.ContainsKey($item.key)) {
                    if ($txt.StartsWith($item.prefix)) {
                        $adj = $para.Range.Information(1)
                        $pageMap[$item.key] = $adj
                        Write-Output "$($item.key) ($($item.prefix)) -> Page $adj (Phys $phys)"
                        break
                    }
                }
            }
        }
    }
}

$jsonPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\page_map.json"
$pageMap | ConvertTo-Json | Set-Content -Path $jsonPath -Encoding utf8
Write-Output "Saved page map to $jsonPath"

$doc.Close(0)
$word.Quit()
