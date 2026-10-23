$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\test_run.pptx", [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
$pres.SaveAs("C:\Users\anand\.gemini\antigravity\scratch\ai_research_paper_assistant\test_run.pdf", 32) # 32 = ppSaveAsPDF
$pres.Close()
$ppt.Quit()
Write-Host "Exported test_run.pdf successfully!"
