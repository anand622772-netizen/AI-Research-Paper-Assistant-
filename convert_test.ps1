$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\test_tbl_hf.docx")
$doc.Fields.Update()
$pdfPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\test_tbl_hf.pdf"
$doc.ExportAsFixedFormat($pdfPath, 17)
$doc.Close(0)
$word.Quit()
Write-Output "Successfully exported test_tbl_hf.pdf"
