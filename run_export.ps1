
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open('C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\parul_university_report\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx')
$doc.Fields.Update()
$pdfPath = 'C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\parul_university_report\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.pdf'
$doc.ExportAsFixedFormat($pdfPath, 17)
$pages = $doc.ComputeStatistics(2)
Write-Output "Word reports total physical pages: $pages"
$doc.Close(0)
$word.Quit()
Write-Output "PDF Export completed successfully."
