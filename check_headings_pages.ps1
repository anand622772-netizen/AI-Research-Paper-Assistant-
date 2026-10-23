$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
$doc = $word.Documents.Open($docPath)
$doc.Fields.Update()

$totalPages = $doc.ComputeStatistics(2)
Write-Output "Total pages in document: $totalPages"

# Let's inspect sections and headings
$targets = @(
    "1. About Department of MScIT",
    "1.1 Overview",
    "1.2 Department Vision",
    "1.3 State-of-the-Art",
    "1.4 Academic Relevance",
    "2. Project Profile",
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
    "3. Requirement Analysis",
    "3.1 Feasibility Study",
    "3.2 Users of the System",
    "3.3 Modules Specification",
    "3.4 Process Model",
    "3.5 Hardware & Software",
    "3.6 Use Cases",
    "3.7 Use Case Diagram",
    "4. Design",
    "4.1 Use Case Scenarios",
    "4.2 Diagrams",
    "4.2.1 UML and Data Flow Diagrams",
    "4.2.1.1 UML Class Diagram",
    "4.2.1.2 UML Sequence Diagram",
    "4.2.1.3 UML Activity Diagram",
    "4.2.2 Entity Relationship Diagram",
    "4.3 Screenshots of Website",
    "4.4 Data Dictionary",
    "5. Implementation",
    "5.1 Form Layouts",
    "5.2 Report Layouts",
    "5.3 Coding Convention",
    "6. Testing",
    "6.1 Test Strategy",
    "6.2 Test Cases Matrix",
    "7. Future Enhancements",
    "8. Bibliography"
)

foreach ($para in $doc.Paragraphs) {
    $txt = $para.Range.Text.Trim()
    foreach ($t in $targets) {
        if ($txt -like "$t*") {
            $page = $para.Range.Information(3) # wdActiveEndPageNumber
            Write-Output "SECTION: $t ===> PAGE $page"
            break
        }
    }
}

$doc.Close($false)
$word.Quit()
