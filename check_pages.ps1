$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = "C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\Parul_University_Minor_Project_Report_AI_Research_Paper_Assistant.docx"
$doc = $word.Documents.Open($docPath)
$pages = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
Write-Host "Page Count: $pages"
$doc.Close()
$word.Quit()
