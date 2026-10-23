$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\parul_university_report\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
$doc = $word.Documents.Open($docPath)
$doc.Fields.Update()

Write-Output "Scanning headings in Word..."

$headings = @(
    "1. ABOUT DEPARTMENT OF MScIT",
    "1.1 Overview",
    "1.2 Department Vision",
    "1.3 State-of-the-Art",
    "1.4 Academic Relevance",
    "2. PROJECT PROFILE",
    "2.1 Project Definition",
    "2.2 Project Description",
    "2.3 Existing System",
    "2.4 Problem Statements",
    "2.5 Need for New System",
    "2.6 Proposed System",
    "2.7 Scope",
    "2.8 Outcomes",
    "2.9 Tools & Technology",
    "2.10 Project Plan",
    "3. REQUIREMENT ANALYSIS",
    "3.1 Feasibility Study",
    "3.2 Users of the System",
    "3.3 Modules",
    "3.4 Process Model",
    "3.5 Hardware & Software",
    "3.6 Use Cases",
    "3.7 Use Case Diagram",
    "4. DESIGN",
    "4.1 Use Case Scenarios",
    "4.2 Diagrams",
    "4.2.1",
    "4.2.2 Entity Relationship",
    "4.3 Screenshots of Website",
    "4.4 Data Dictionary",
    "5. IMPLEMENTATION",
    "5.1 Form Layouts",
    "5.2 Report Layouts",
    "5.3 Coding Convention",
    "6. TESTING",
    "6.1 Test Strategy",
    "6.2 Test Cases Matrix",
    "7. FUTURE ENHANCEMENTS",
    "8. BIBLIOGRAPHY"
)

# Single pass over paragraphs:
$results = @{}
foreach ($para in $doc.Paragraphs) {
    $t = $para.Range.Text.Trim()
    if ($t.Length -gt 0) {
        foreach ($h in $headings) {
            if (-not $results.ContainsKey($h)) {
                if ($t.StartsWith($h) -or $t -like "*$h*") {
                    # wdActiveEndAdjustedPageNumber = 1
                    # wdActiveEndPageNumber = 3
                    $adjPage = $para.Range.Information(1)
                    $physPage = $para.Range.Information(3)
                    $results[$h] = @{ Adj = $adjPage; Phys = $physPage }
                    Write-Output "$h -> Adjusted Page: $adjPage (Physical Page: $physPage)"
                    break
                }
            }
        }
    }
}

$doc.Close(0)
$word.Quit()
