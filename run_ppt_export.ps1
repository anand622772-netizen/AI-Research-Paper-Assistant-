
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open('C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\presentation\Parul_University_Minor_Project_AI_Research_Paper_Assistant.pptx')
$pres.SaveAs('C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\outputs\presentation\Parul_University_Minor_Project_AI_Research_Paper_Assistant.pdf', 32)
$pres.Close()
$ppt.Quit()
Write-Host "PDF export finished."
