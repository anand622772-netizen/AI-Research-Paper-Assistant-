$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
$doc = $word.Documents.Open($docPath)
$doc.Fields.Update()

$indexItems = @(
    @{no="1."; desc="About Department of MScIT"; prefix="1. About Department of MScIT"},
    @{no=""; desc="1.1 Overview of Department of MScIT & Faculty of IT & CS"; prefix="1.1 Overview"},
    @{no=""; desc="1.2 Department Vision, Mission, and Quality Policy"; prefix="1.2 Department Vision"},
    @{no=""; desc="1.3 State-of-the-Art Laboratory Infrastructure & Clusters"; prefix="1.3 State-of-the-Art"},
    @{no=""; desc="1.4 Academic Relevance and Minor Project Framework"; prefix="1.4 Academic Relevance"},
    @{no="2."; desc="Project Profile"; prefix="2. Project Profile"},
    @{no=""; desc="2.1 Project Definition"; prefix="2.1 Project Definition"},
    @{no=""; desc="2.2 Project Description"; prefix="2.2 Project Description"},
    @{no=""; desc="2.3 Existing System / Work Environment"; prefix="2.3 Existing System"},
    @{no=""; desc="2.4 Problem Statements"; prefix="2.4 Problem Statements"},
    @{no=""; desc="2.5 Need for New System"; prefix="2.5 Need for New System"},
    @{no=""; desc="2.6 Proposed System & Features"; prefix="2.6 Proposed System"},
    @{no=""; desc="2.7 Scope"; prefix="2.7 Scope"},
    @{no=""; desc="2.8 Outcomes"; prefix="2.8 Outcomes"},
    @{no=""; desc="2.9 Tools & Technology Used"; prefix="2.9 Tools & Technology"},
    @{no=""; desc="2.10 Project Plan"; prefix="2.10 Project Plan"},
    @{no="3."; desc="Requirement Analysis"; prefix="3. Requirement Analysis"},
    @{no=""; desc="3.1 Feasibility Study (Technical, Economic, Operational, Legal)"; prefix="3.1 Feasibility Study"},
    @{no=""; desc="3.2 Users of the System"; prefix="3.2 Users of the System"},
    @{no=""; desc="3.3 Modules Specification"; prefix="3.3 Modules Specification"},
    @{no=""; desc="3.4 Process Model (Agile Iterative Framework)"; prefix="3.4 Process Model"},
    @{no=""; desc="3.5 Hardware & Software Requirements"; prefix="3.5 Hardware & Software"},
    @{no=""; desc="3.6 Use Cases"; prefix="3.6 Use Cases"},
    @{no=""; desc="3.7 Use Case Diagram"; prefix="3.7 Use Case Diagram"},
    @{no="4."; desc="Design"; prefix="4. Design"},
    @{no=""; desc="4.1 Use Case Scenarios (UC-01 to UC-06 Detailed Matrices)"; prefix="4.1 Use Case Scenarios"},
    @{no=""; desc="4.2 Diagrams"; prefix="4.2 Diagrams"},
    @{no=""; desc="4.2.1 Data Flow Diagrams (DFD Level 0, 1, 2, 3) & UML Diagrams"; prefix="4.2.1 UML and Data Flow Diagrams"},
    @{no=""; desc="4.2.2 Entity Relationship Diagram (ER Diagram)"; prefix="4.2.2 Entity Relationship Diagram"},
    @{no=""; desc="4.3 Screenshots of Website & User Interface Walkthrough"; prefix="4.3 Screenshots of Website"},
    @{no=""; desc="4.4 Data Dictionary (Entities, Schema Attributes & Types)"; prefix="4.4 Data Dictionary"},
    @{no="5."; desc="Implementation"; prefix="5. Implementation"},
    @{no=""; desc="5.1 Form Layouts"; prefix="5.1 Form Layouts"},
    @{no=""; desc="5.2 Report Layouts (Manuscript, BibTeX, Peer Review, ZIP)"; prefix="5.2 Report Layouts"},
    @{no=""; desc="5.3 Coding Convention (Business Logic Implementations)"; prefix="5.3 Coding Convention"},
    @{no="6."; desc="Testing"; prefix="6. Testing"},
    @{no=""; desc="6.1 Test Strategy & Environment"; prefix="6.1 Test Strategy"},
    @{no=""; desc="6.2 Test Cases Matrix (16 Verification Test Suites)"; prefix="6.2 Test Cases Matrix"},
    @{no="7."; desc="Future Enhancements"; prefix="7. Future Enhancements"},
    @{no="8."; desc="Bibliography"; prefix="8. Bibliography"}
)

$results = @()
foreach ($item in $indexItems) {
    $foundPage = $null
    foreach ($para in $doc.Paragraphs) {
        $p = $para.Range.Information(3)
        if ($p -ge 7) {
            $txt = $para.Range.Text.Trim()
            if ($txt.StartsWith($item.prefix)) {
                $foundPage = $para.Range.Information(1)
                break
            }
        }
    }
    if ($foundPage -eq $null) {
        $foundPage = "NOT FOUND"
    }
    $results += [PSCustomObject]@{
        No = $item.no
        Desc = $item.desc
        Prefix = $item.prefix
        ActualPage = $foundPage
    }
}

$results | Format-Table -AutoSize | Out-String | Write-Output

$doc.Close($false)
$word.Quit()
