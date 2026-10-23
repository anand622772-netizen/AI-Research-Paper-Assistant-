$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("C:\Users\anand\AppData\Local\Programs\antigravity\test_run.pptx")
$pres.SaveAs("C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\test_run.pdf", 32)
$pres.Close()
$ppt.Quit()
Write-Host "Exported 1-slide presentation to PDF successfully!"
